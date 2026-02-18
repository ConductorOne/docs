# Client Credentials Authentication

Create a service principal, generate credentials, and make API calls.

## Step 1: Create Service Principal

1. Navigate to Settings > Developers > Service principals
2. Click Create service principal
3. Enter display name (e.g., "Terraform CI")
4. Click Create

## Step 2: Create Credential

1. On service principal detail page, select Credentials tab
2. Click Create credential
3. Configure:
   - **Display name**: Label for this credential
   - **Expiration**: 30, 60, 90, or 180 days (90 recommended)
   - **Limit source IPs**: Optional IP ranges (e.g., `192.168.1.0/24`)
   - **Limit scopes**: Full permissions or specific role
   - **Require DPoP**: Optional proof-of-possession (advanced)
4. Click Create
5. Copy client ID and client secret immediately

**Important**: Secret shown only once. Starts with `secret-token:` - this prefix is part of the value.

## Step 3: Get Access Token

```bash
curl -s -X POST "https://yourcompany.conductor.one/auth/v1/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=clever-fox-42195@yourcompany.conductor.one/spc" \
  -d "client_secret=secret-token:YOUR_SECRET_HERE"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJFZERTQSIs...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## Step 4: Call API

```bash
curl -s "https://yourcompany.conductor.one/api/v1/apps" \
  -H "Authorization: Bearer ${CONDUCTORONE_ACCESS_TOKEN}"
```

## Token Endpoint

`https://{tenant}.conductor.one/auth/v1/token`

Grant type: `client_credentials`

Token lifetime: 1 hour (3600 seconds)
