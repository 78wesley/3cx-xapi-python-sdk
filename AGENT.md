# AGENT.md — 3CX Python SDK

Guide for AI agents working on this codebase.

## What this project is

A typed Python SDK for the **3CX XAPI** (`/xapi/v1`).  The API is an OData v4 service that controls a 3CX PBX: calls, users, queues, ring groups, trunks, phones, reporting, and system settings.  The authoritative spec is `swagger.yaml` (OpenAPI 3.0.4, ~39 000 lines).

Authentication: **OAuth2 client credentials** (`POST /connect/token`).

## Repository layout

```
3cx-flow/
├── swagger.yaml             # Full API spec — reference only, not used at runtime
├── pyproject.toml           # Build metadata, dependencies, tool config
├── README.md                # End-user documentation
├── CLAUDE.md                # Claude Code project instructions
├── AGENT.md                 # This file
└── threecx/                 # SDK package
    ├── __init__.py           # Public re-exports: ThreeCXClient, OAuth2Auth, ODataQuery, exceptions
    ├── client.py             # ThreeCXClient — owns the httpx.Client lifetime, registers all services
    ├── auth.py               # OAuth2Auth — httpx.Auth subclass, caches token, auto-refreshes 30s before expiry
    ├── exceptions.py         # ThreeCXError hierarchy + raise_for_status() dispatcher
    ├── odata.py              # ODataQuery — fluent builder for all OData query parameters
    ├── models/
    │   ├── base.py           # ODataCollection[T] (generic envelope), ODataError
    │   ├── calls.py          # ActiveCall, CallHistoryEntry, OutboundCall
    │   ├── users.py          # User, Group, ForwardingProfile, Greeting
    │   ├── queues.py         # Queue, QueueAgent, QueueManager, RingGroup, RingGroupMember
    │   ├── trunks.py         # Trunk, Peer, Sbc
    │   ├── contacts.py       # Contact
    │   ├── phones.py         # Phone, PhoneTemplate
    │   └── system.py         # SystemStatus, LicenseStatus, SystemParameters
    └── services/
        ├── base.py           # BaseService: _get/_post/_patch/_delete, _paginate()
        ├── active_calls.py   # list(), iterate(), drop(id)
        ├── users.py          # list/iterate/create/get/update/delete + groups/greetings/make_call/batch_delete
        ├── queues.py         # list/iterate/create/get/update/delete + agents/managers/reset_statistics
        ├── ring_groups.py    # list/iterate/create/get/update/delete
        ├── call_history.py   # list(), iterate(), count()
        ├── trunks.py         # trunks + peers + SBCs (get/create/update/delete per resource)
        ├── contacts.py       # list/iterate/create/get/update/delete
        ├── phones.py         # phones + templates + reboot/reprovision
        ├── system.py         # status/license/parameters + raw get/post escape hatches
        └── reports.py        # call log, extension stats, queue performance, agent login, activity log
```

## Key design decisions

### 1. Single shared `httpx.Client`
`ThreeCXClient` creates one `httpx.Client` (sync, not async) and passes it to every service.  The client is the bearer of the `base_url`, auth, timeout, and TLS settings.  This means all services automatically use the same token refresh cycle and connection pool.

### 2. `OAuth2Auth` as an `httpx.Auth` subclass
Token acquisition is transparent.  Any service method that makes an HTTP call will trigger `auth_flow()`, which ensures a valid token is present before the request goes out.  Token is cached in `_Token(access_token, expires_at)` and refreshed 30 s before actual expiry.

### 3. `BaseService` centralises all HTTP concerns
Every service extends `BaseService` and calls `_get`, `_post`, `_patch`, `_delete`.  These methods call `_raise()` which maps HTTP error codes to typed exceptions via `raise_for_status()`.

### 4. `list()` vs `iterate()`
- `list()` — makes one request, returns `List[Model]`.  Fast; use when you know results fit in one page or you control `$top`.
- `iterate()` — generator; follows `@odata.nextLink` automatically until exhausted.  Use for bulk exports.

### 5. Models are wire-compatible via aliases
Pydantic fields use `alias="PascalCase"` to match the 3CX API's casing.  Python code uses `snake_case` attributes.  When sending data to the API, always call `model.model_dump(by_alias=True, exclude_none=True)`.

### 6. Report endpoints return raw dicts
The 30+ report schemas are highly specialised and change per report type.  `ReportsService` returns `List[Dict[str, Any]]` so callers can use them with pandas, custom Pydantic models, or just iterate the raw JSON.

## How to look up an API endpoint

The swagger spec is too large to read at once.  Use grep:

```bash
# Find a path
grep -n "^  /Recordings" swagger.yaml

# Find an operationId
grep -n "operationId: GetRecording" swagger.yaml

# Find a schema
grep -n "^    Pbx.Recording:" swagger.yaml
```

Then read that section with `Read` using `offset` + `limit`.

## How to add a new service

### Step 1 — Identify the endpoints

```bash
grep -n "^  /MyResource" swagger.yaml
```

Note the HTTP methods, path parameter names, request body schemas, and response schemas.

### Step 2 — Write or extend a model

In `threecx/models/<domain>.py`:

```python
from .base import _Base
from pydantic import Field
from typing import Optional

class MyEntity(_Base):
    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
```

Export it from `threecx/models/__init__.py`.

### Step 3 — Write the service

In `threecx/services/<domain>.py`:

```python
from .base import BaseService
from ..models.<domain> import MyEntity
from ..odata import ODataQuery
from typing import List, Optional

class MyResourceService(BaseService):
    _PATH = "/MyResource"

    def list(self, query: Optional[ODataQuery] = None) -> List[MyEntity]:
        data = self._list_raw(self._PATH, query)
        return [MyEntity.model_validate(item) for item in data.get("value", [])]

    def get(self, entity_id: int) -> MyEntity:
        data = self._get(f"{self._PATH}({entity_id})")
        return MyEntity.model_validate(data)
```

### Step 4 — Register in client

In `threecx/client.py`, add to `__init__`:

```python
from .services.<domain> import MyResourceService
# ...
self.my_resource = MyResourceService(self._http)
```

Export from `threecx/services/__init__.py`.

## OData URL patterns (from swagger.yaml)

| Pattern | Example |
|---|---|
| Collection | `GET /Users` |
| By integer key | `GET /Users(101)` |
| By string key | `GET /Queues(Number='200')` |
| Action (POST, side-effect) | `POST /Users(101)/Pbx.SendWelcomeEmail` |
| Action with body | `POST /Users/Pbx.BatchDelete` + JSON body |
| Function (GET, path params) | `GET /Users/Pbx.GetFirstAvailableExtensionNumber()` |
| Function with params | `GET /ActivityLog/Pbx.GetLogs(startDate=...,endDate=...,...)` |

## Exception hierarchy

```
ThreeCXError
├── AuthenticationError   (401)
├── NotFoundError         (404)
├── ValidationError       (400, 422)
├── RateLimitError        (429)
└── ServerError           (5xx)
```

All exceptions carry `.status_code` and `.detail` (raw response body).

## Testing approach

Tests live in `tests/` (not yet created).  Use `pytest-httpx` to mock the `httpx.Client`:

```python
import pytest
from pytest_httpx import HTTPXMock
from threecx import ThreeCXClient

@pytest.fixture
def client(httpx_mock: HTTPXMock):
    # mock the token endpoint
    httpx_mock.add_response(
        url="https://pbx.test/connect/token",
        json={"access_token": "tok", "expires_in": 3600},
    )
    return ThreeCXClient("https://pbx.test", "id", "secret")

def test_list_users(client, httpx_mock):
    httpx_mock.add_response(
        url="https://pbx.test/xapi/v1/Users",
        json={"value": [{"Id": 1, "Number": "100", "FirstName": "Alice"}]},
    )
    users = client.users.list()
    assert users[0].number == "100"
```

## Dependencies

| Package | Why |
|---|---|
| `httpx>=0.27` | HTTP client; `httpx.Auth` protocol for transparent token injection |
| `pydantic>=2.0` | Model validation, alias mapping, serialisation |

Dev only: `pytest`, `pytest-httpx`, `ruff`, `mypy`.

## What is out of scope

- Async support (not implemented; the API is sync)
- All 177 resource groups — only the most common ~10 have typed services; use `client.get()` / `client.post()` for the rest
- Websocket / push notifications (not part of XAPI)
