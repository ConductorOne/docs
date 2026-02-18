# debug-errors

Common errors and their solutions.

---

## Pagination Loop Detected

**Error:** `pagination loop detected: same token returned`

**Cause:** Your List/Grants method returned the same next token twice.

**Fix:**
```go
// Wrong
return resources, currentToken, nil, nil

// Right - return NEW token or empty string
if hasMore {
    return resources, newToken, nil, nil
}
return resources, "", nil, nil
```

## Authentication Failures

**Error:** `401 Unauthorized` or `403 Forbidden`

**Causes:**
- Token expired
- Token lacks required scopes
- Wrong API endpoint

**Fix:**
1. Verify token is valid: `curl -H "Authorization: Bearer $TOKEN" $API_URL`
2. Check required scopes in target system docs
3. Regenerate token with correct permissions

## Rate Limiting

**Error:** `429 Too Many Requests`

**Cause:** Hitting API rate limits.

**Fix:** The SDK's uhttp client handles retries automatically. If still failing:
- Reduce page size
- Add delays between requests
- Request rate limit increase from API provider

## Empty Sync Results

**Symptom:** Connector runs successfully but `baton resources` shows nothing.

**Causes:**
- Credentials lack read permissions
- API returns empty due to filters
- Wrong base URL

**Fix:**
1. Test API directly with curl
2. Check if filters in code exclude everything
3. Verify base URL matches environment (prod vs staging)

## Connection Refused

**Error:** `connection refused` or `no such host`

**Causes:**
- Wrong hostname
- Firewall blocking connection
- Service is down

**Fix:**
1. Verify URL is correct
2. Test connectivity: `curl -v $API_URL`
3. Check firewall/VPN requirements

## Certificate Errors

**Error:** `x509: certificate signed by unknown authority`

**Cause:** Self-signed or internal CA certificate.

**Fix for testing:**
```go
// Add to client setup
client.WithInsecureSkipVerify(true)
```

**Production fix:** Add CA certificate to trust store.

## JSON Parsing Errors

**Error:** `json: cannot unmarshal...`

**Cause:** API response doesn't match expected structure.

**Fix:**
1. Log raw response: `--log-level debug`
2. Compare actual response to struct definition
3. Handle optional/nullable fields

## Missing Entitlements

**Symptom:** Resources exist but no entitlements appear.

**Cause:** Entitlements() method returns empty.

**Fix:** Verify Entitlements() returns at least one entitlement for resources that should offer permissions.

## Grants Not Appearing

**Symptom:** Entitlements exist but no grants.

**Causes:**
- Grants() not implemented
- Principal resource type doesn't exist
- Wrong entitlement ID in grant

**Fix:**
1. Verify Grants() is called (add logging)
2. Check principal resource type matches a synced type
3. Verify entitlement ID matches what Entitlements() returns
