from __future__ import annotations

from typing import Optional

from pydantic import Field

from .base import _Base


class Contact(_Base):
    """Represents a PBX contact book entry (Pbx.Contact)."""

    id: Optional[int] = Field(None, alias="Id")
    first_name: Optional[str] = Field(None, alias="FirstName")
    last_name: Optional[str] = Field(None, alias="LastName")
    company_name: Optional[str] = Field(None, alias="CompanyName")
    email: Optional[str] = Field(None, alias="Email")
    phone_number: Optional[str] = Field(None, alias="PhoneNumber")
    mobile: Optional[str] = Field(None, alias="Mobile2")
    home: Optional[str] = Field(None, alias="Home")
    business: Optional[str] = Field(None, alias="Business")
    title: Optional[str] = Field(None, alias="Title")
    department: Optional[str] = Field(None, alias="Department")
    tag: Optional[str] = Field(None, alias="Tag")
    contact_type: Optional[str] = Field(None, alias="ContactType")

    @property
    def full_name(self) -> str:
        parts = filter(None, [self.first_name, self.last_name])
        return " ".join(parts)
