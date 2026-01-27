# IP/CIDR Functions

Functions for network-based access control using IP addresses and CIDR ranges.

## ip()

Create an IP address object from a string.

```cel
ip(address: string) -> IPAddr
```

**Example:**
```cel
ip("192.168.1.100")
ip(ctx.trigger.source_ip)
```

---

## cidr()

Create a CIDR range or set of ranges.

```cel
cidr(range: string) -> CIDRSet
cidr(ranges: list<string>) -> CIDRSet
cidr(range1: string, range2: string, ...) -> CIDRSet
```

**Example:**
```cel
// Single range
cidr("10.0.0.0/8")

// Multiple ranges
cidr("10.0.0.0/8", "192.168.0.0/16")
cidr(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"])
```

---

## contains()

Check if an IP is within a CIDR range.

```cel
cidrSet.contains(ip: IPAddr) -> bool
```

**Example:**
```cel
// Check if request is from corporate network
cidr("10.0.0.0/8").contains(ip(ctx.trigger.source_ip))
```

---

## Common Patterns

### Corporate Network Check

```cel
has(ctx.trigger.source_ip) &&
  cidr("10.0.0.0/8", "192.168.0.0/16").contains(ip(ctx.trigger.source_ip))
```

### RFC 1918 Private Addresses

```cel
cidr(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]).contains(ip(source_ip))
```

### VPN/Office Detection

```cel
// Requests from VPN get different approval flow
has(ctx.trigger.source_ip) &&
  cidr("10.50.0.0/16").contains(ip(ctx.trigger.source_ip))
```

---

## Availability

IP/CIDR functions are available in workflow/automation contexts where `ctx.trigger.source_ip` provides the request origin. Not typically used in dynamic groups or basic policy conditions.
