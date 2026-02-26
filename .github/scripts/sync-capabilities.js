#!/usr/bin/env node

/**
 * Sync Capabilities Matrix
 *
 * This script parses specified connector documentation files and compares their
 * stated capabilities against the capabilities matrix in capabilities.mdx.
 * If mismatches are found, it updates the matrix and outputs a summary.
 *
 * Usage: node sync-capabilities.js [file1.mdx] [file2.mdx] ...
 *
 * Detection is based on explicit statements in connector docs:
 * - Account provisioning: "account provisioning" or Accounts row with Provision checkmark
 * - Account deprovisioning: "and deprovisioning" or "deprovision" without negation
 * - Entitlement provisioning: Non-account resources with Provision checkmark
 */

const fs = require('fs');
const path = require('path');

const BATON_DIR = path.join(__dirname, '../../baton');
const CAPABILITIES_FILE = path.join(BATON_DIR, 'capabilities.mdx');

/**
 * Parse the capabilities table from a connector doc
 * Returns structured info about what can be provisioned
 */
function parseCapabilitiesTable(content) {
  const result = {
    hasTable: false,
    accountsCanProvision: false,
    entitlementsCanProvision: false,
    resources: [],
  };

  // Find the capabilities table
  const tableMatch = content.match(/##\s*Capabilities[\s\S]*?\|[^|]*Resource[^|]*\|[^|]*Sync[^|]*\|[^|]*Provision[^|]*\|([\s\S]*?)(?=\n\n|\n##|\n<)/i);

  if (!tableMatch) return result;

  result.hasTable = true;
  const tableContent = tableMatch[0];

  // Parse each row
  const rowRegex = /^\|\s*([^|]+)\s*\|([^|]*)\|([^|]*)\|/gm;
  let match;

  while ((match = rowRegex.exec(tableContent)) !== null) {
    const resource = match[1].trim();
    const provisionCol = match[3];

    // Skip header row
    if (resource.toLowerCase() === 'resource' || resource.startsWith(':') || resource.startsWith('-')) {
      continue;
    }

    const canProvision = provisionCol.includes('square-check');
    result.resources.push({ resource, canProvision });

    // Check if this is accounts provisioning
    if (/^accounts?$/i.test(resource) && canProvision) {
      result.accountsCanProvision = true;
    }

    // Check for entitlement-type resources (non-accounts that can be provisioned)
    if (!/^accounts?$/i.test(resource) && canProvision) {
      result.entitlementsCanProvision = true;
    }
  }

  return result;
}

/**
 * Parse a connector doc file and extract capabilities
 */
function parseConnectorDoc(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const fileName = path.basename(filePath, '.mdx');

  // Parse the capabilities table first
  const tableInfo = parseCapabilitiesTable(content);

  const capabilities = {
    fileName,
    cloudHosted: false,
    selfHosted: false,
    provisionsEntitlements: false,
    provisionsAccounts: false,
    deprovisionsAccounts: false,
    confidence: 'low',
  };

  // Check for hosting options
  capabilities.cloudHosted = /<Tab\s+title=["']Cloud-hosted["']/i.test(content);
  capabilities.selfHosted = /<Tab\s+title=["']Self-hosted["']/i.test(content);

  // Use table info as primary source
  if (tableInfo.hasTable) {
    capabilities.provisionsAccounts = tableInfo.accountsCanProvision;
    capabilities.provisionsEntitlements = tableInfo.entitlementsCanProvision;
    capabilities.confidence = 'high';
  }

  // Check for account provisioning text (high confidence patterns)
  const hasExplicitAccountProvisioning =
    /supports?\s+(?:\[)?automatic\s+account\s+provisioning/i.test(content) ||
    /connector\s+supports?\s+(?:\[)?(?:automatic\s+)?account\s+provisioning/i.test(content);

  if (hasExplicitAccountProvisioning) {
    capabilities.provisionsAccounts = true;
    capabilities.confidence = 'high';
  }

  // Check for deprovisioning - must have explicit positive mention
  const hasDeprovisioningMention =
    /provisioning\s+and\s+deprovisioning/i.test(content) ||
    /account\s+provisioning\s+and\s+deprovisioning/i.test(content);

  const hasNegativeDeprovisioning =
    /does\s+not\s+support\s+(?:account\s+)?deprovisioning/i.test(content) ||
    /cannot\s+deprovision/i.test(content) ||
    /must\s+deprovision\s+(?:accounts?\s+)?directly/i.test(content);

  if (hasDeprovisioningMention && !hasNegativeDeprovisioning) {
    capabilities.deprovisionsAccounts = true;
  } else if (hasNegativeDeprovisioning) {
    capabilities.deprovisionsAccounts = false;
    capabilities.confidence = 'high';
  }

  return capabilities;
}

/**
 * Parse the capabilities matrix and extract current state
 */
function parseCapabilitiesMatrix(content) {
  const connectors = new Map();

  // Match table rows (skip header and separator)
  const tableRegex = /^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|$/gm;
  let match;

  while ((match = tableRegex.exec(content)) !== null) {
    const [fullMatch, name, link, hosting, provisioning, other] = match;

    // Extract the file name from the link
    const linkMatch = link.match(/\/baton\/([^)]+)/);
    const fileName = linkMatch ? linkMatch[1] : null;

    if (!fileName) continue;

    connectors.set(fileName, {
      name,
      link,
      fullMatch,
      hosting: {
        cloud: hosting.includes('icon="cloud"'),
        selfHosted: hosting.includes('icon="plug"'),
      },
      provisioning: {
        entitlements: provisioning.includes('icon="key"'),
        accounts: provisioning.includes('icon="user"'),
        deprovisions: provisioning.includes('icon="face-confused"'),
      },
      other: {
        secrets: other.includes('icon="face-shush"'),
        ticketing: other.includes('icon="ticket"'),
        lastLogin: other.includes('icon="clock"'),
        passwords: other.includes('rect x="3" y="11"'),
        shadowApps: other.includes('icon="flashlight"'),
      },
      rawHosting: hosting.trim(),
      rawProvisioning: provisioning.trim(),
      rawOther: other.trim(),
    });
  }

  return connectors;
}

/**
 * Build the provisioning cell icons string
 */
function buildProvisioningIcons(caps) {
  const icons = [];
  if (caps.provisionsEntitlements) icons.push('<Icon icon="key" />');
  if (caps.provisionsAccounts) icons.push('<Icon icon="user" />');
  if (caps.deprovisionsAccounts) icons.push('<Icon icon="face-confused" />');
  return icons.join(' ');
}

/**
 * Compare detected capabilities with matrix and find mismatches
 * Only report mismatches where we have high confidence in the doc parsing
 */
function findMismatches(docCaps, matrixCaps) {
  const mismatches = [];

  // Only report mismatches for deprovisioning, which is more reliably detected
  if (docCaps.deprovisionsAccounts !== matrixCaps.provisioning.deprovisions) {
    mismatches.push({
      field: 'deprovisioning (face-confused icon)',
      doc: docCaps.deprovisionsAccounts,
      matrix: matrixCaps.provisioning.deprovisions,
    });
  }

  // Only report account provisioning if we have high confidence
  if (docCaps.confidence === 'high' &&
      docCaps.provisionsAccounts !== matrixCaps.provisioning.accounts) {
    mismatches.push({
      field: 'accounts (user icon)',
      doc: docCaps.provisionsAccounts,
      matrix: matrixCaps.provisioning.accounts,
    });
  }

  // Only report entitlement provisioning if we have a capabilities table
  if (docCaps.confidence === 'high' &&
      docCaps.provisionsEntitlements !== matrixCaps.provisioning.entitlements) {
    mismatches.push({
      field: 'entitlements (key icon)',
      doc: docCaps.provisionsEntitlements,
      matrix: matrixCaps.provisioning.entitlements,
    });
  }

  return mismatches;
}

/**
 * Main function
 */
function main() {
  // Get files to process from command line arguments
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(JSON.stringify({
      hasChanges: false,
      mismatchCount: 0,
      summary: 'No connector files specified.',
      mismatches: [],
    }, null, 2));
    return;
  }

  // Read capabilities matrix
  const matrixContent = fs.readFileSync(CAPABILITIES_FILE, 'utf-8');
  const matrixConnectors = parseCapabilitiesMatrix(matrixContent);

  const allMismatches = [];
  let updatedContent = matrixContent;

  for (const filePath of args) {
    // Handle both relative and absolute paths
    const fullPath = path.isAbsolute(filePath) ? filePath : path.join(process.cwd(), filePath);

    if (!fs.existsSync(fullPath)) {
      console.error(`Warning: File not found: ${fullPath}`);
      continue;
    }

    const fileName = path.basename(fullPath, '.mdx');

    // Skip non-connector files
    if (fileName === 'capabilities' || fileName.startsWith('_') || fileName.startsWith('baton-')) {
      continue;
    }

    // Parse the connector doc
    const docCaps = parseConnectorDoc(fullPath);

    // Find the connector in the matrix
    const matrixEntry = matrixConnectors.get(fileName);

    if (!matrixEntry) {
      // Connector not in matrix - skip
      continue;
    }

    // Compare capabilities
    const mismatches = findMismatches(docCaps, matrixEntry);

    if (mismatches.length > 0) {
      allMismatches.push({
        connector: matrixEntry.name,
        fileName,
        mismatches,
        docCaps,
        matrixEntry,
      });

      // Build the updated provisioning icons based on what the doc says
      const updatedCaps = {
        provisionsEntitlements: mismatches.find(m => m.field.includes('entitlements'))
          ? docCaps.provisionsEntitlements
          : matrixEntry.provisioning.entitlements,
        provisionsAccounts: mismatches.find(m => m.field.includes('accounts'))
          ? docCaps.provisionsAccounts
          : matrixEntry.provisioning.accounts,
        deprovisionsAccounts: mismatches.find(m => m.field.includes('deprovisioning'))
          ? docCaps.deprovisionsAccounts
          : matrixEntry.provisioning.deprovisions,
      };

      const newProvisioningIcons = buildProvisioningIcons(updatedCaps);

      // Update the row
      const newRow = matrixEntry.fullMatch.replace(
        /\|([^|]*)\|([^|]*)\|$/,
        `| ${newProvisioningIcons} |$2|`
      );

      updatedContent = updatedContent.replace(matrixEntry.fullMatch, newRow);
    }
  }

  // Write updated content if there are changes
  const hasChanges = allMismatches.length > 0;

  if (hasChanges) {
    fs.writeFileSync(CAPABILITIES_FILE, updatedContent);
  }

  // Build summary
  let summary = '';
  if (hasChanges) {
    for (const { connector, fileName, mismatches } of allMismatches) {
      summary += `### ${connector}\n`;
      summary += `File: \`baton/${fileName}.mdx\`\n\n`;
      for (const m of mismatches) {
        const docStatus = m.doc ? 'supports' : 'does not support';
        const matrixStatus = m.matrix ? 'shows' : 'does not show';
        summary += `- **${m.field}**: Documentation says connector ${docStatus} this, but matrix ${matrixStatus} it\n`;
      }
      summary += '\n';
    }
  } else {
    summary = 'No mismatches found. The capabilities matrix is in sync with the checked connector docs.';
  }

  // Output result as JSON
  const result = {
    hasChanges,
    mismatchCount: allMismatches.length,
    summary,
    mismatches: allMismatches.map(m => ({
      connector: m.connector,
      fileName: m.fileName,
      issues: m.mismatches,
    })),
  };

  console.log(JSON.stringify(result, null, 2));
}

main();
