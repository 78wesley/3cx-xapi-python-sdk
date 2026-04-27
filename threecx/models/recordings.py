from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class Recording(_Base):
    """Represents a call recording (Pbx.Recording)."""

    id: Optional[int] = Field(None, alias="Id")
    caller: Optional[str] = Field(None, alias="Caller")
    callee: Optional[str] = Field(None, alias="Callee")
    start_time: Optional[str] = Field(None, alias="StartTime")
    duration: Optional[int] = Field(None, alias="Duration")
    file_name: Optional[str] = Field(None, alias="FileName")
    file_size: Optional[int] = Field(None, alias="FileSize")
    transcribed: Optional[bool] = Field(None, alias="Transcribed")
