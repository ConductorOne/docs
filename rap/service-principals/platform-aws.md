# AWS IAM Integration

Use AWS IAM outbound identity federation for secretless authentication from AWS workloads.

## Prerequisites

- Service principal with AWS IAM federation trust (use AWS IAM Outbound preset)
- Trust's client ID (e.g., `calm-wolf-40291@yourcompany.conductor.one/wfe`)
- Outbound identity federation enabled in AWS account

## AWS Setup

### Enable outbound identity federation

```bash
aws iam enable-outbound-web-identity-federation
aws iam get-outbound-web-identity-federation-info
```

Returns account-specific issuer URL (e.g., `https://abc123-def456.tokens.sts.global.api.aws`). Use this as the provider issuer URL in C1.

### IAM permissions

Attach policy granting `sts:GetWebIdentityToken` with audience condition:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:GetWebIdentityToken",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "sts:Audience": "yourcompany.conductor.one"
        }
      }
    }
  ]
}
```

## Token Exchange

```bash
# Get JWT from AWS STS
AWS_JWT=$(aws sts get-web-identity-token \
  --audience yourcompany.conductor.one \
  --query 'Token' --output text)

# Exchange for ConductorOne access token
C1_ACCESS_TOKEN=$(curl -s -X POST \
  "https://yourcompany.conductor.one/auth/v1/token" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  -d "subject_token=$AWS_JWT" \
  -d "subject_token_type=urn:ietf:params:oauth:token-type:jwt" \
  -d "client_id=calm-wolf-40291@yourcompany.conductor.one/wfe" \
  | jq -r '.access_token')
```

When using C1 tools (`cone`, Terraform provider), you must set these environment variables. Do not skip this step — the tools require both to be set to handle the token exchange internally:

```bash
export CONDUCTORONE_OIDC_TOKEN=$AWS_JWT
export CONDUCTORONE_CLIENT_ID=calm-wolf-40291@yourcompany.conductor.one/wfe

cone whoami
terraform apply
```

## CEL Expressions

### Restrict to AWS account
```
claims["https://sts.amazonaws.com/"]["aws_account"] == "123456789012"
```

### Restrict to specific IAM role
```
claims.sub == "arn:aws:iam::123456789012:role/DeployRole"
```

### Restrict to account and organization
```
claims["https://sts.amazonaws.com/"]["aws_account"] == "123456789012" && claims["https://sts.amazonaws.com/"]["org_id"] == "o-abc1234567"
```

### Restrict using principal tags
```
claims["https://sts.amazonaws.com/"]["principal_tags"]["environment"] == "production"
```

## AWS OIDC Claims

### Standard claims

| Claim | Example | Description |
|-------|---------|-------------|
| `sub` | `arn:aws:iam::123456789012:role/DeployRole` | IAM principal ARN |
| `iss` | `https://abc123-def456.tokens.sts.global.api.aws` | Account-specific issuer URL |
| `aud` | `yourcompany.conductor.one` | Audience from token request |

### AWS identity claims (under `https://sts.amazonaws.com/`)

| Claim | Example | Description |
|-------|---------|-------------|
| `aws_account` | `123456789012` | AWS account ID |
| `source_region` | `us-east-1` | Token request region |
| `org_id` | `o-abc1234567` | AWS Organizations ID |
| `ou_path` | `o-a1b2c3d4e5/r-ab12/ou-ab12-11111111/` | Organizational unit path |
| `principal_tags` | `{"environment": "production"}` | IAM principal tags |

### Session context claims (under `https://sts.amazonaws.com/`)

| Claim | Example | Description |
|-------|---------|-------------|
| `ec2_source_instance_arn` | `arn:aws:ec2:us-east-1:123456789012:instance/i-abc123` | EC2 instance ARN |
| `lambda_source_function_arn` | `arn:aws:lambda:us-east-1:123456789012:function/my-func` | Lambda function ARN |
| `source_identity` | `admin-user` | Source identity |
| `request_tags` | `{"team": "platform"}` | Custom tags from token request |

## Security

Bind to specific AWS account ID and IAM role ARN. Use principal tags and organization constraints for defense-in-depth. Limit token lifetime via IAM policy. Use scoped roles on trust.
