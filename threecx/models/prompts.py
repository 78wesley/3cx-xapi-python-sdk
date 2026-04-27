from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from .base import _Base


class PromptSet(_Base):
    """Represents a set of system prompts (Pbx.PromptSet)."""

    id: Optional[int] = Field(None, alias="Id")
    name: Optional[str] = Field(None, alias="Name")
    language: Optional[str] = Field(None, alias="Language")
    is_active: Optional[bool] = Field(None, alias="IsActive")
    prompts: Optional[List[Any]] = Field(None, alias="Prompts")


class Playlist(_Base):
    """Represents a music-on-hold playlist (Pbx.Playlist)."""

    name: Optional[str] = Field(None, alias="Name")
    files: Optional[List[Any]] = Field(None, alias="Files")
    repeat: Optional[bool] = Field(None, alias="Repeat")
    shuffle: Optional[bool] = Field(None, alias="Shuffle")
