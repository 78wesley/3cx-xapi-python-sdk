from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class Weblink(_Base):
    """Represents a website link (Pbx.Weblink)."""

    link: Optional[str] = Field(None, alias="Link")
    name: Optional[str] = Field(None, alias="Name")
    description: Optional[str] = Field(None, alias="Description")
    enabled: Optional[bool] = Field(None, alias="Enabled")
