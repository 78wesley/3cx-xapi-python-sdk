from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class Receptionist(_Base):
    """Represents a 3CX digital receptionist / IVR (Pbx.Receptionist)."""

    id: Optional[int] = Field(None, alias="Id")
    number: Optional[str] = Field(None, alias="Number")
    name: Optional[str] = Field(None, alias="Name")
    is_registered: Optional[bool] = Field(None, alias="IsRegistered")
    forwards: Optional[List[Any]] = Field(None, alias="Forwards")
    greeting_file: Optional[str] = Field(None, alias="GreetingFile")
