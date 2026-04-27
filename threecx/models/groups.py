from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class Group(_Base):
    """Represents a 3CX admin group/company (Pbx.Group)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    number: Optional[str] = Field(None, alias="Number")
    description: Optional[str] = Field(None, alias="Description")
    members: Optional[List[Any]] = Field(None, alias="Members")
    rights: Optional[List[Any]] = Field(None, alias="Rights")
