# Service Principals Documentation Index

Documentation for ConductorOne service principals and workload federation. Request relevant sections based on user's question.

## How to Use

1. Read user's question
2. Identify relevant sections (up to 3-4)
3. Request those files
4. Answer using retrieved content

## Available Sections

### Conceptual

| Section | File | Covers |
|---------|------|--------|
| What service principals are | `concepts-overview.md` | Machine identities, when to use, auth methods comparison |
| Environment variables | `concepts-env-vars.md` | CONDUCTORONE_* variables, priority order |

### Client Credentials

| Section | File | Covers |
|---------|------|--------|
| Client credentials flow | `auth-client-credentials.md` | Create credential, get token, API calls |
| Terraform and Cone CLI | `auth-tools.md` | Provider config, CLI usage |

### Workload Federation

| Section | File | Covers |
|---------|------|--------|
| Federation concepts | `federation-overview.md` | Providers, trusts, token exchange, CEL |
| Setting up federation | `federation-setup.md` | Wizard walkthrough, test tokens |
| GitHub Actions | `platform-github.md` | oidc-token-action, CEL claims, examples |
| GitLab CI | `platform-gitlab.md` | id_tokens, curl exchange, CEL claims |
| HCP Terraform | `platform-terraform.md` | Workspace config, provider setup, CEL claims |
| Custom OIDC | `platform-custom.md` | Generic token exchange, provider requirements |

### Security

| Section | File | Covers |
|---------|------|--------|
| Security controls | `security-controls.md` | Scoped roles, IP allowlists, expiration, DPoP |
| CEL expressions | `security-cel.md` | Writing expressions, claims, examples |
| Audit events | `security-audit.md` | System log events, authentication, API activity |

### Management

| Section | File | Covers |
|---------|------|--------|
| Lifecycle management | `manage-lifecycle.md` | View, edit, disable, delete |
| Credential rotation | `manage-credentials.md` | Rotation procedure, revoking |
| Ownership and permissions | `manage-permissions.md` | Owners, roles, capabilities |

---

## Selection Guidelines

**"How do I..."**
- Authenticate automation -> `concepts-overview.md`, `auth-client-credentials.md`
- Set up GitHub Actions -> `platform-github.md`
- Set up GitLab CI -> `platform-gitlab.md`
- Set up HCP Terraform -> `platform-terraform.md`
- Use custom OIDC provider -> `platform-custom.md`
- Create a service principal -> `auth-client-credentials.md`
- Create a federation trust -> `federation-setup.md`
- Rotate credentials -> `manage-credentials.md`
- Restrict IP addresses -> `security-controls.md`
- Write CEL expressions -> `security-cel.md`
- View audit logs -> `security-audit.md`

**"What is..."**
- A service principal -> `concepts-overview.md`
- Workload federation -> `federation-overview.md`
- A provider vs trust -> `federation-overview.md`
- CEL -> `security-cel.md`
- DPoP -> `security-controls.md`
- Scoped roles -> `security-controls.md`

**Configuration**
- Environment variables -> `concepts-env-vars.md`
- Terraform provider -> `auth-tools.md`
- Cone CLI -> `auth-tools.md`

**Troubleshooting**
- Token exchange fails -> `federation-setup.md`, `security-cel.md`
- IP blocked -> `security-controls.md`
- Credential expired -> `manage-credentials.md`
- CEL not matching -> `security-cel.md`

---

## Usage Examples

User: "How do I authenticate from GitHub Actions?"
Retrieve: `platform-github.md`

User: "Set up Terraform with ConductorOne"
Retrieve: `auth-tools.md`, `platform-terraform.md`

User: "Rotate service principal credentials"
Retrieve: `manage-credentials.md`

User: "CEL expression for specific repository"
Retrieve: `security-cel.md`, `platform-github.md`

User: "What environment variables does ConductorOne use?"
Retrieve: `concepts-env-vars.md`

User: "Difference between client credentials and workload federation"
Retrieve: `concepts-overview.md`
