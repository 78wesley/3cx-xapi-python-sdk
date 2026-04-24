from __future__ import annotations
from typing import Any


class ThreeCXError(Exception):
    """Base exception for all 3CX SDK errors."""

    def __init__(self, message: str, status_code: int | None = None, detail: Any = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code}, message={str(self)!r})"


class AuthenticationError(ThreeCXError):
    """Raised when OAuth2 token acquisition or refresh fails."""


class NotFoundError(ThreeCXError):
    """Raised on HTTP 404."""


class ValidationError(ThreeCXError):
    """Raised on HTTP 400 / 422."""


class ServerError(ThreeCXError):
    """Raised on HTTP 5xx."""


class RateLimitError(ThreeCXError):
    """Raised on HTTP 429."""


def raise_for_status(status_code: int, body: Any) -> None:
    message = _extract_message(body)
    if status_code == 401:
        raise AuthenticationError(message, status_code, body)
    if status_code == 404:
        raise NotFoundError(message, status_code, body)
    if status_code in (400, 422):
        raise ValidationError(message, status_code, body)
    if status_code == 429:
        raise RateLimitError(message, status_code, body)
    if status_code >= 500:
        raise ServerError(message, status_code, body)
    if status_code >= 400:
        raise ThreeCXError(message, status_code, body)


def _extract_message(body: Any) -> str:
    if isinstance(body, dict):
        err = body.get("error", body)
        if isinstance(err, dict):
            return err.get("message", str(body))
        return str(err)
    return str(body)
