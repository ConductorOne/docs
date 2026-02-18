# CEL in Terraform

CEL expressions in the ConductorOne Terraform provider.

## Resources Supporting CEL

| Resource | Attribute | Purpose |
|----------|-----------|---------|
| `conductorone_policy` | `rules[].condition` | Route requests to policy steps |
| `conductorone_policy` | `expression_approval.expressions[]` | Dynamic approver selection |
| `conductorone_policy` | `wait_condition.condition` | Wait step conditions |
| `conductorone_access_review` | `cel_expression_scope.expression` | Filter users in scope |

---

## Policy Rule Conditions

Route requests to different approval workflows:

```hcl
resource "conductorone_policy" "contractor_policy" {
  display_name = "Contractor Access Policy"

  rules = [
    {
      condition  = "subject.employment_type == \"contractor\""
      policy_key = "contractor_approval"
    },
    {
      condition  = "entitlement.app_resource_type == \"Production\""
      policy_key = "production_approval"
    }
  ]

  policy_steps = {
    contractor_approval = {
      steps = [
        # ... approval steps
      ]
    }
    production_approval = {
      steps = [
        # ... approval steps
      ]
    }
  }
}
```

---

## Expression-Based Approvers

Dynamically select who approves:

```hcl
resource "conductorone_policy" "dynamic_approval" {
  display_name = "Dynamic Approval Policy"

  policy_steps = {
    default = {
      steps = [
        {
          approval = {
            expression_approval = {
              expressions = [
                "c1.directory.users.v1.GetManagers(subject)",
                "appOwners"
              ]
              allow_self_approval = false
              fallback            = true
              fallback_user_ids   = ["fallback-admin-user-id"]
            }
          }
        }
      ]
    }
  }
}
```

First non-empty result is used. Enable `fallback` for safety.

---

## Wait Conditions

Pause until a condition is met:

```hcl
resource "conductorone_policy" "wait_for_manager" {
  display_name = "Policy with Wait Condition"

  policy_steps = {
    default = {
      steps = [
        {
          wait = {
            name             = "Wait for manager assignment"
            timeout_duration = "24h"
            wait_condition = {
              condition = "has(subject.manager_id)"
            }
          }
        },
        {
          approval = {
            manager_approval = {
              allow_self_approval = false
            }
          }
        }
      ]
    }
  }
}
```

---

## Access Review Scopes

Filter which users are reviewed:

```hcl
resource "conductorone_access_review" "engineering_review" {
  display_name = "Engineering Quarterly Review"

  access_review_scope_v2 = {
    cel_expression_scope = {
      expression = "subject.department == \"Engineering\""
    }
  }
}
```

---

## HCL Quoting

CEL expressions in HCL require escaped quotes:

```hcl
# Escaped quotes
condition = "subject.department == \"Engineering\""

# Heredoc for complex expressions (easier to read)
condition = <<-EOT
  subject.department == "Engineering" &&
  subject.job_title.contains("Manager")
EOT
```

---

## Tips

1. **Validate in UI first** - Test expressions in the ConductorOne UI before deploying via Terraform
2. **Use heredoc for readability** - Complex expressions are easier to read with heredoc syntax
3. **Check return types** - Conditions return `bool`, approvers return `User`/`list<User>`
