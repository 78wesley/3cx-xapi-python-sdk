from __future__ import annotations

from ._generated import Contact as _Contact


class Contact(_Contact):
    @property
    def full_name(self) -> str:
        parts = filter(None, [self.first_name, self.last_name])
        return " ".join(parts)


__all__ = ["Contact"]
