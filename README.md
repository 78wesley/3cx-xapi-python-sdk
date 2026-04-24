# 3CX Python SDK

A typed Python SDK for the **3CX XAPI** (`/xapi/v1`), built on [httpx](https://www.python-httpx.org/) and [Pydantic v2](https://docs.pydantic.dev/latest/).

## Features

- **OAuth2 client-credentials** authentication with automatic token refresh
- **OData v4** query builder (`$filter`, `$select`, `$expand`, `$orderby`, `$top`, `$skip`, `$count`)
- Automatic **pagination** — iterate over all pages with a single generator call
- Full **CRUD** for users, queues, ring groups, trunks, contacts, and phones
- Reporting helpers for call log, queue performance, extension statistics, activity log, and more
- **Context-manager** support for clean resource management
- Escape hatches (`client.get()` / `client.post()`) for any unlisted endpoint

## Installation

```bash
pip install threecx-sdk
```

Or directly from source:

```bash
pip install .
```

## Quick start

```python
from threecx import ThreeCXClient, ODataQuery

client = ThreeCXClient(
    base_url="https://pbx.example.com",
    client_id="<service-principal-client-id>",
    client_secret="<service-principal-secret>",
)

# ── Active calls ─────────────────────────────────────────────────────────────
for call in client.active_calls.list():
    print(f"{call.caller} → {call.callee}  (duration: {call.duration}s)")

# Drop a specific call
client.active_calls.drop(call_id=42)

# ── Users ─────────────────────────────────────────────────────────────────────
# List first 50 enabled users, sorted by extension number
q = ODataQuery().filter("Enabled eq true").order_by("Number").top(50)
for user in client.users.list(q):
    print(user.number, user.full_name, user.email)

# Get a single user and update their e-mail
user = client.users.get(101)
client.users.update(101, {"Email": "new@example.com"})

# Create a user
from threecx.models import User
new_user = client.users.create(User(
    Number="200",
    FirstName="Alice",
    LastName="Smith",
    Email="alice@example.com",
))

# ── Queues ────────────────────────────────────────────────────────────────────
for queue in client.queues.list():
    agents = client.queues.get_agents(queue.id)
    print(f"Queue {queue.name}: {len(agents)} agents")

# ── Call history ──────────────────────────────────────────────────────────────
q = ODataQuery().filter("CallDirection eq 'Inbound'").order_by("StartTime desc").top(100)
for entry in client.call_history.iterate(q):
    print(entry.start_time, entry.caller, "→", entry.callee, entry.status)

# ── Reports ───────────────────────────────────────────────────────────────────
from datetime import datetime, timedelta, timezone

end = datetime.now(timezone.utc)
start = end - timedelta(days=7)
rows = client.reports.get_call_log(start, end)
print(f"{len(rows)} call-log entries for the last 7 days")

# ── System status ─────────────────────────────────────────────────────────────
status = client.system.get_status()
print(f"PBX {status.pbx_version}  calls: {status.calls_active}  cpu: {status.cpu_usage}%")

# ── Context manager ───────────────────────────────────────────────────────────
with ThreeCXClient(base_url="https://pbx.example.com",
                   client_id="...", client_secret="...") as c:
    print(c.system.get_license())
```

## OData query builder

```python
from threecx import ODataQuery

q = (
    ODataQuery()
    .filter("LastName eq 'Smith'")
    .select("Id", "Number", "FirstName", "LastName", "Email")
    .expand("Groups")
    .order_by("Number")
    .top(25)
    .skip(0)
    .count()
)
```

All query parameters map directly to OData v4 syntax. Refer to the [3CX XAPI swagger](swagger.yaml) for supported fields per endpoint.

## Creating a service principal

1. Log in to 3CX as admin.
2. Navigate to **Admin → Integrations → API**.
3. Create a new service principal and copy the **Client ID** and **Client Secret**.

## Services reference

| `client.<service>` | Resource |
|---|---|
| `active_calls` | `/ActiveCalls` — list & drop live calls |
| `users` | `/Users` — CRUD extensions/users |
| `queues` | `/Queues` — CRUD call queues & agents |
| `ring_groups` | `/RingGroups` — CRUD ring groups |
| `call_history` | `/CallHistoryView` — paginated call log |
| `trunks` | `/Trunks`, `/Peers`, `/Sbcs` |
| `contacts` | `/Contacts` — company phone book |
| `phones` | `/Phones`, `/PhoneTemplates` — IP phones |
| `system` | `/SystemStatus`, `/LicenseStatus`, `/Parameters` |
| `reports` | Call log, queue & extension statistics, activity log |

## Escape hatch

Any endpoint not covered by a typed service can be called directly:

```python
data = client.get("/InboundRules", params={"$top": "10"})
result = client.post("/Backups/Pbx.CreateBackup")
```
