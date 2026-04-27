from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class Fax(_Base):
    """Represents a fax extension (Pbx.Fax)."""

    id: Optional[int] = Field(None, alias="Id")
    number: Optional[str] = Field(None, alias="Number")
    name: Optional[str] = Field(None, alias="Name")
    is_registered: Optional[bool] = Field(None, alias="IsRegistered")
    email: Optional[str] = Field(None, alias="Email")
    enabled: Optional[bool] = Field(None, alias="Enabled")
