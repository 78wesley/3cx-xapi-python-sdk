from __future__ import annotations

from ._generated import ForwardingProfile, Greeting, UserGroup
from ._generated import User as _User


class User(_User):
    @property
    def full_name(self) -> str:
        parts = filter(None, [self.first_name, self.last_name])
        return " ".join(parts)


UserGroupRef = UserGroup
Group = UserGroup

__all__ = ["User", "UserGroup", "UserGroupRef", "Group", "ForwardingProfile", "Greeting"]
