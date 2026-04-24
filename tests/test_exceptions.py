"""Unit tests for the exception hierarchy and raise_for_status."""
from __future__ import annotations

import pytest

from threecx.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ThreeCXError,
    ValidationError,
    _extract_message,
    raise_for_status,
)


# --- _extract_message ---------------------------------------------------------

def test_extract_message_plain_string():
    assert _extract_message("oops") == "oops"


def test_extract_message_dict_with_error_string():
    assert _extract_message({"error": "invalid_client"}) == "invalid_client"


def test_extract_message_dict_with_error_object():
    body = {"error": {"message": "User not found", "code": "404"}}
    assert _extract_message(body) == "User not found"


def test_extract_message_dict_no_error_key():
    body = {"someOtherKey": "value"}
    result = _extract_message(body)
    assert "someOtherKey" in result


def test_extract_message_non_string():
    assert _extract_message(42) == "42"


# --- raise_for_status ---------------------------------------------------------

@pytest.mark.parametrize("code,exc_type", [
    (401, AuthenticationError),
    (404, NotFoundError),
    (400, ValidationError),
    (422, ValidationError),
    (429, RateLimitError),
    (500, ServerError),
    (503, ServerError),
])
def test_raise_for_status_maps_codes(code: int, exc_type: type) -> None:
    with pytest.raises(exc_type) as exc_info:
        raise_for_status(code, {"error": {"message": "test error"}})
    assert exc_info.value.status_code == code


def test_raise_for_status_generic_4xx():
    with pytest.raises(ThreeCXError) as exc_info:
        raise_for_status(409, "conflict")
    assert exc_info.value.status_code == 409


def test_raise_for_status_no_raise_on_2xx():
    raise_for_status(200, {})   # must not raise
    raise_for_status(204, None)  # must not raise


# --- Exception attributes -----------------------------------------------------

def test_exception_carries_status_code():
    err = AuthenticationError("bad token", status_code=401, detail={"x": 1})
    assert err.status_code == 401
    assert err.detail == {"x": 1}
    assert str(err) == "bad token"


def test_exception_repr():
    err = NotFoundError("missing", status_code=404)
    assert "404" in repr(err)
    assert "NotFoundError" in repr(err)


def test_is_subclass_of_base():
    assert issubclass(AuthenticationError, ThreeCXError)
    assert issubclass(NotFoundError, ThreeCXError)
    assert issubclass(ServerError, ThreeCXError)
