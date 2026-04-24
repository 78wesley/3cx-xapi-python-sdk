from __future__ import annotations

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class _Base(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )


class ODataCollection(_Base, Generic[T]):
    """Generic OData collection response envelope."""

    odata_context: Optional[str] = Field(None, alias="@odata.context")
    odata_count: Optional[int] = Field(None, alias="@odata.count")
    odata_next_link: Optional[str] = Field(None, alias="@odata.nextLink")
    value: List[T] = Field(default_factory=list)

    @property
    def count(self) -> Optional[int]:
        return self.odata_count

    @property
    def next_link(self) -> Optional[str]:
        return self.odata_next_link


class ODataError(_Base):
    code: Optional[str] = None
    message: Optional[str] = None
    target: Optional[str] = None
    details: Optional[List[Any]] = None
    innererror: Optional[Any] = None
