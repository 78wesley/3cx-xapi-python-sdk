from __future__ import annotations

import time
from dataclasses import dataclass, field

import httpx

from .exceptions import AuthenticationError


@dataclass
class _Token:
    access_token: str
    expires_at: float


@dataclass
class OAuth2Auth(httpx.Auth):
    """OAuth2 client-credentials authenticator for the 3CX XAPI.

    Tokens are cached and refreshed automatically when they expire.

    Args:
        base_url: Base URL of the 3CX instance, e.g. ``https://pbx.example.com``.
        client_id: Service-principal client ID.
        client_secret: Service-principal client secret.
        token_path: Path to the token endpoint (default: ``/connect/token``).
    """

    base_url: str
    client_id: str
    client_secret: str
    token_path: str = "/connect/token"
    _token: _Token | None = field(default=None, init=False, repr=False)

    # --- httpx.Auth protocol --------------------------------------------------

    def auth_flow(self, request: httpx.Request):
        token = self._get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

    # --- internal helpers -----------------------------------------------------

    def _get_token(self) -> str:
        if self._token is None or time.monotonic() >= self._token.expires_at:
            self._token = self._fetch_token()
        return self._token.access_token

    def _fetch_token(self) -> _Token:
        url = self.base_url.rstrip("/") + self.token_path
        try:
            response = httpx.post(
                url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        except httpx.HTTPError as exc:
            raise AuthenticationError(f"Token request failed: {exc}") from exc

        if response.status_code != 200:
            raise AuthenticationError(
                f"Token endpoint returned {response.status_code}: {response.text}",
                response.status_code,
            )

        data = response.json()
        if "access_token" not in data:
            raise AuthenticationError(f"No access_token in response: {data}")

        expires_in = int(data.get("expires_in", 3600))
        # Subtract 30 s to refresh before actual expiry
        expires_at = time.monotonic() + expires_in - 30
        return _Token(access_token=data["access_token"], expires_at=expires_at)

    def invalidate(self) -> None:
        """Force the next request to re-acquire a token."""
        self._token = None
