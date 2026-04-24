from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.users import ForwardingProfile, Greeting, Group, User
from ..odata import ODataQuery
from .base import BaseService


class UsersService(BaseService):
    """CRUD operations for PBX users/extensions.

    Reference paths:
      GET    /Users
      POST   /Users
      GET    /Users({Id})
      PATCH  /Users({Id})
      DELETE /Users({Id})
      GET    /Users({Id})/Groups
      GET    /Users({Id})/ForwardingProfiles
      GET    /Users({Id})/Greetings
      POST   /Users({Id})/Pbx.SendWelcomeEmail
      POST   /Users/Pbx.BatchDelete
      POST   /Users/Pbx.MakeCall
    """

    _PATH = "/Users"

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def list(self, query: Optional[ODataQuery] = None) -> List[User]:
        """Return all users (single page)."""
        data = self._list_raw(self._PATH, query)
        return [User.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[User]:
        """Yield users across all OData pages."""
        yield from self._paginate(self._PATH, User, query)

    def create(self, user: User | Dict[str, Any]) -> User:
        """Create a new user/extension."""
        payload = user.model_dump(by_alias=True, exclude_none=True) if isinstance(user, User) else user
        data = self._post(self._PATH, json=payload)
        return User.model_validate(data)

    # ------------------------------------------------------------------
    # Single entity
    # ------------------------------------------------------------------

    def get(
        self,
        user_id: int,
        query: Optional[ODataQuery] = None,
    ) -> User:
        """Retrieve a user by numeric ID."""
        data = self._get(f"{self._PATH}({user_id})", params=self._query_params(query))
        return User.model_validate(data)

    def update(self, user_id: int, changes: User | Dict[str, Any]) -> None:
        """Partially update a user (PATCH)."""
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, User) else changes
        self._patch(f"{self._PATH}({user_id})", json=payload)

    def delete(self, user_id: int, etag: Optional[str] = None) -> None:
        """Delete a user by ID. Optionally pass an ETag for optimistic concurrency."""
        self._delete(f"{self._PATH}({user_id})", etag=etag)

    # ------------------------------------------------------------------
    # Sub-resources
    # ------------------------------------------------------------------

    def get_groups(self, user_id: int) -> List[Group]:
        data = self._get(f"{self._PATH}({user_id})/Groups")
        return [Group.model_validate(item) for item in data.get("value", [])]

    def get_forwarding_profiles(self, user_id: int) -> List[ForwardingProfile]:
        data = self._get(f"{self._PATH}({user_id})/ForwardingProfiles")
        return [ForwardingProfile.model_validate(item) for item in data.get("value", [])]

    def get_greetings(self, user_id: int) -> List[Greeting]:
        data = self._get(f"{self._PATH}({user_id})/Greetings")
        return [Greeting.model_validate(item) for item in data.get("value", [])]

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def send_welcome_email(self, user_id: int) -> None:
        """Send the welcome e-mail to a user."""
        self._post(f"{self._PATH}({user_id})/Pbx.SendWelcomeEmail")

    def make_call(self, user_id: int, destination: str) -> None:
        """Initiate a click-to-call for the user towards *destination*."""
        self._post(f"{self._PATH}({user_id})/Pbx.MakeCall", json={"Destination": destination})

    def batch_delete(self, user_ids: List[int]) -> None:
        """Delete multiple users in one request."""
        self._post(f"{self._PATH}/Pbx.BatchDelete", json={"userIds": user_ids})

    def regenerate_passwords(self) -> None:
        """Trigger password regeneration for all users."""
        self._post(f"{self._PATH}/Pbx.RegeneratePasswords")

    def get_first_available_extension(self) -> str:
        """Return the next free extension number."""
        data = self._get(f"{self._PATH}/Pbx.GetFirstAvailableExtensionNumber()")
        return data.get("value", data)
