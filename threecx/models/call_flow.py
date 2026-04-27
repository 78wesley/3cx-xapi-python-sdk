from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class CallFlowApp(_Base):
    """Represents a Call Flow App (Pbx.CallFlowApp)."""

    id: Optional[int] = Field(None, alias="Id")
    number: Optional[str] = Field(None, alias="Number")
    name: Optional[str] = Field(None, alias="Name")
    is_registered: Optional[bool] = Field(None, alias="IsRegistered")
    files: Optional[List[Any]] = Field(None, alias="Files")
