# debug-workflow

Step-by-step process for debugging connector issues.

---

## 1. Run Locally First

```bash
./baton-myservice --api-token "$TOKEN" -f sync.c1z
```

Check exit code. Non-zero means error.

## 2. Inspect the Output

```bash
# What resources were synced?
baton resources -f sync.c1z

# What grants exist?
baton grants -f sync.c1z

# What entitlements are available?
baton entitlements -f sync.c1z

# Stats overview
baton stats -f sync.c1z
```

## 3. Increase Log Verbosity

```bash
./baton-myservice --api-token "$TOKEN" --log-level debug -f sync.c1z
```

Debug logs show:
- API requests and responses
- Pagination state
- Resource counts per type

## 4. Check for Common Issues

**Zero resources?**
- Credentials may lack read permissions
- API endpoint may be wrong
- Filter may be excluding everything

**Missing grants?**
- Check Grants() method is implemented
- Verify entitlements exist on resources
- Check pagination isn't truncating results

**Pagination loop?**
- Your next token isn't progressing
- See error: "pagination loop detected"

## 5. Test Individual Endpoints

If the connector calls multiple APIs, test each:

```bash
# Test with curl first
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/v1/users | jq .
```

## 6. Review Resource Mapping

Resources may exist but not match expected types:

```bash
# List specific resource type
baton resources -f sync.c1z --resource-type user

# Look for unexpected types
baton resources -f sync.c1z | sort | uniq -c
```

## 7. Validate Against Production

Compare local sync to production:
- Same resource counts?
- Same grant patterns?
- Any missing resource types?

## Debugging Checklist

| Symptom | Check |
|---------|-------|
| No resources | Credentials, API endpoint, filters |
| No grants | Grants() implementation, entitlements exist |
| Pagination loop | Token progression logic |
| Missing users | User list endpoint, status filters |
| Wrong counts | Page size, pagination completeness |
| Auth failures | Token validity, required scopes |
