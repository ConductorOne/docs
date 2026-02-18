# Ownership and Permissions

Who can manage service principals and what they can do.

## Ownership

Each service principal has one or more owners.

Owners can:
- Edit display name
- Create, update, revoke credentials
- Create, update, delete federation trusts
- Delete the service principal

Manage owners on service principal detail page in Owners section.

## Role Capabilities

| Role | Capabilities |
|------|-------------|
| Super Admin | Create, view, edit, delete service principals. Create and manage providers. View all trusts and credentials. Full access. |
| Service principal owner | View, edit, delete owned service principal. Manage its credentials and trusts. Cannot create new service principals. |
| Authenticated user | View list of service principals (metadata only). Cannot create, edit, or manage credentials. |

## Provider Management

Workload federation provider management restricted to Super Admins.

Owners can create trusts using existing providers but cannot create new providers.

## Creating Service Principals

Only Super Admins can create new service principals.

Once created, Super Admin can assign owners who then manage independently.

## Assigning Roles

Service principals are assigned ConductorOne roles like human users. Role assignment controlled by Super Admins.

Credentials and trusts can further restrict effective permissions via scoped roles (intersection of assigned roles and scoped roles).
