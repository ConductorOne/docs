# CEL Expressions

CEL (Common Expression Language) controls which federation tokens are accepted.

## How It Works

Expression evaluated against JWT claims. Must return `true` for token to be accepted.

## Environment

Available in CEL:
- `claims` - map of all decoded JWT claims

Standard string functions:
- `contains()`
- `startsWith()`
- `endsWith()`
- `matches()`
- `size()`

## Example Expressions

| Provider | Expression |
|----------|------------|
| GitHub Actions | `claims.repository == "acme/infra" && claims.environment == "production"` |
| GitLab CI | `claims.project_path == "acme/infra" && claims.ref_protected == "true"` |
| HCP Terraform | `claims.terraform_organization == "acme" && claims.terraform_workspace_name == "infra-prod"` |
| AWS IAM | `claims["https://sts.amazonaws.com/"].aws_account == "123456789012"` |

## Writing Expressions

**Always validate `sub` or equivalent identifier.**

Use additional claims for defense-in-depth:
- Repository/project
- Branch/ref
- Environment
- Run phase

### Namespaced Claims

For claims with URL namespaces (like AWS):
```
claims["https://sts.amazonaws.com/"].field
```

## Limits

- Max expression size: 1,024 bytes

## Testing

Use Test CEL tool at Settings > Workload Federation to validate expressions against sample claims without a real JWT.

## Common Patterns

### Exact match
```
claims.repository == "acme/infra"
```

### Multiple conditions
```
claims.repository == "acme/infra" && claims.environment == "production"
```

### String contains
```
claims.repository.contains("infra")
```

### String prefix
```
claims.ref.startsWith("refs/heads/release/")
```

### Regex match
```
claims.ref.matches("^refs/heads/(main|release/.*)$")
```

## Troubleshooting

If token exchange fails with `cel_condition_not_met`:
1. Check claim names match exactly (case-sensitive)
2. Verify claim values in your JWT
3. Test expression with Test CEL tool
4. Check for typos in string literals
