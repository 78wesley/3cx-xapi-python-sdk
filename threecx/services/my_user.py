from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..models.users import ForwardingProfile, Greeting, User, UserGroupRef
from ..odata import ODataQuery
from .base import BaseService


class MyUserService(BaseService):
    _PATH = "/MyUser"

    def get(self, query: Optional[ODataQuery] = None) -> User:
        data = self._get(self._PATH, params=self._query_params(query))
        return User.model_validate(data)

    def update(self, changes: User | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, User) else changes
        self._patch(self._PATH, json=payload)

    def get_forwarding_profiles(self) -> List[ForwardingProfile]:
        data = self._get(f"{self._PATH}/ForwardingProfiles")
        return [ForwardingProfile.model_validate(item) for item in data.get("value", [])]

    def get_greetings(self) -> List[Greeting]:
        data = self._get(f"{self._PATH}/Greetings")
        return [Greeting.model_validate(item) for item in data.get("value", [])]

    def get_groups(self) -> List[UserGroupRef]:
        data = self._get(f"{self._PATH}/Groups")
        return [UserGroupRef.model_validate(item) for item in data.get("value", [])]

    def generate_prov_link(self) -> str:
        data = self._get(f"{self._PATH}/Pbx.GenerateProvLink()")
        return str(data.get("value", ""))
