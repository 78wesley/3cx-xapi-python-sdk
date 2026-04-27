from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class Holiday(_Base):
    """Represents a PBX holiday entry (Pbx.Holiday)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    date: Optional[str] = Field(None, alias="Date")
    recurring: Optional[bool] = Field(None, alias="Recurring")
