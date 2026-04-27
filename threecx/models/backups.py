from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class BackupEntry(_Base):
    """Represents a backup file entry (Pbx.Backup)."""

    file_name: Optional[str] = Field(None, alias="FileName")
    created: Optional[str] = Field(None, alias="Created")
    size: Optional[int] = Field(None, alias="Size")
    version: Optional[str] = Field(None, alias="Version")
