# 3CX Python SDK

A typed Python SDK for the **3CX XAPI** (`/xapi/v1`), built on [httpx](https://www.python-httpx.org/) and [Pydantic v2](https://docs.pydantic.dev/latest/).

## Features

- **OAuth2 client-credentials** authentication with automatic token refresh
- **OData v4** query builder (`$filter`, `$select`, `$expand`, `$orderby`, `$top`, `$skip`, `$count`)
- Automatic **pagination** — iterate over all pages with a single generator call
- **Full coverage** — 37 typed services covering every resource group in the 3CX XAPI swagger spec
- Reporting helpers for call log, queue performance, extension statistics, activity log, and more
- **Context-manager** support for clean resource management
- Escape hatches (`client.get()` / `client.post()`) for raw access to any endpoint

## Installation

```bash
pip install 3cx-xapi-python-sdk
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

The SDK exposes **37 services** as attributes of `ThreeCXClient`, covering every resource group in `swagger.yaml`.

### Calls & telephony
| `client.<service>` | Resource |
|---|---|
| `active_calls` | `/ActiveCalls` — list & drop live calls |
| `call_history` | `/CallHistoryView` — paginated call log |
| `recordings` | `/Recordings`, `/RemoteArchivingSettings` |
| `voicemail` | `/VoicemailSettings`, `/MusicOnHoldSettings` |
| `fax` | `/Fax`, `/FaxServerSettings` |

### Users, groups & directories
| `client.<service>` | Resource |
|---|---|
| `users` | `/Users` — CRUD extensions/users + greetings, phones, provisioning |
| `my_user` | `/MyUser` — current authenticated user |
| `groups` | `/Groups` — full admin groups (members, rights, restrictions) |
| `my_group` | `/MyGroup` — current user's primary group |
| `contacts` | `/Contacts` — company phone book |
| `parameters` | `/TenantProperties`, `/DNProperties`, directory info |

### Call routing & flow
| `client.<service>` | Resource |
|---|---|
| `queues` | `/Queues` — CRUD call queues & agents |
| `ring_groups` | `/RingGroups` — CRUD ring groups |
| `inbound_rules` | `/InboundRules` — DID/inbound rules |
| `outbound_rules` | `/OutboundRules` — outbound dial rules |
| `receptionists` | `/Receptionists` — digital receptionists |
| `holidays` | `/Holidays`, `/OfficeHours` |
| `parkings` | `/Parkings`, `/CallParkingSettings` |
| `call_flow` | `/CallFlowApps`, `/CallFlowScripts` |

### Trunks & PBX hardware
| `client.<service>` | Resource |
|---|---|
| `trunks` | `/Trunks`, `/TrunkTemplates`, `/Peers`, `/Sbcs` |
| `phones` | `/Phones`, `/PhoneTemplates`, `/SipDevices`, `/Fxs`, `/FxsTemplates`, `/DeviceInfos`, `/Firmwares` |

### Communication
| `client.<service>` | Resource |
|---|---|
| `chat` | `/ChatHistoryView`, `/ChatMessagesHistoryView` |
| `prompts` | `/PromptSets`, `/CustomPrompts`, `/Playlists` |
| `email` | `/EmailTemplate` |

### System administration
| `client.<service>` | Resource |
|---|---|
| `system` | `/SystemStatus`, `/LicenseStatus`, `/Parameters` |
| `settings` | `/GeneralSettingsForPbx`, `/MailSettings`, `/CDRSettings`, ~20 settings domains |
| `pbx_services` | `/Services` — start/stop/enable/disable PBX services |
| `backups` | `/Backups`, failover & restore settings |
| `updates` | `/Updates`, prompt set / CRM updates, Debian upgrade |
| `event_logs` | `/EventLogs` |
| `security` | `/SecurityTokens`, `/ServicePrincipals`, `/BlackListNumbers`, `/Blocklist`, `/AntiHackingSettings`, `/Firewall` |
| `emergency` | `/EmergencyGeoLocations`, `/EmergencyNotificationsSettings` |
| `defs` | `/Defs` — codecs, timezones, gateway parameters, countries, DID numbers |

### Integrations
| `client.<service>` | Resource |
|---|---|
| `integrations` | `/Microsoft365Integration`, `/Microsoft365TeamsIntegration`, `/GoogleSettings`, `/AmazonIntegrationSettings`, `/DataConnectorSettings`, `/AISettings` |
| `crm` | `/CrmIntegration`, `/CrmTemplates` |
| `website_links` | `/WebsiteLinks` |

### Reporting
| `client.<service>` | Resource |
|---|---|
| `reports` | 30+ report endpoints: call log, queue & extension statistics, agent login, activity log, SLA breaches, audit, scheduled reports |

## Escape hatch

Any endpoint not covered by a typed service can be called directly:

```python
data = client.get("/InboundRules", params={"$top": "10"})
result = client.post("/Backups/Pbx.CreateBackup")
```
