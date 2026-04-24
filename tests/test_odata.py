"""Unit tests for ODataQuery — no HTTP required."""
from __future__ import annotations

import pytest

from threecx.odata import ODataQuery


def test_empty_query_produces_no_params():
    assert ODataQuery().to_params() == {}


def test_top():
    assert ODataQuery().top(25).to_params() == {"$top": 25}


def test_skip():
    assert ODataQuery().skip(50).to_params() == {"$skip": 50}


def test_count_default_true():
    assert ODataQuery().count().to_params() == {"$count": "true"}


def test_count_false():
    assert ODataQuery().count(False).to_params() == {"$count": "false"}


def test_select_single():
    assert ODataQuery().select("Id").to_params() == {"$select": "Id"}


def test_select_multiple():
    params = ODataQuery().select("Id", "FirstName", "LastName").to_params()
    assert params["$select"] == "Id,FirstName,LastName"


def test_expand():
    assert ODataQuery().expand("Groups", "Greetings").to_params() == {
        "$expand": "Groups,Greetings"
    }


def test_filter():
    params = ODataQuery().filter("Enabled eq true").to_params()
    assert params["$filter"] == "Enabled eq true"


def test_search():
    assert ODataQuery().search("alice").to_params() == {"$search": "alice"}


def test_order_by_single():
    assert ODataQuery().order_by("Number").to_params() == {"$orderby": "Number"}


def test_order_by_multiple():
    params = ODataQuery().order_by("LastName", "FirstName").to_params()
    assert params["$orderby"] == "LastName,FirstName"


def test_chaining_all_params():
    q = (
        ODataQuery()
        .filter("Enabled eq true")
        .select("Id", "Number")
        .expand("Groups")
        .order_by("Number")
        .top(10)
        .skip(20)
        .count()
    )
    params = q.to_params()
    assert params["$filter"] == "Enabled eq true"
    assert params["$select"] == "Id,Number"
    assert params["$expand"] == "Groups"
    assert params["$orderby"] == "Number"
    assert params["$top"] == 10
    assert params["$skip"] == 20
    assert params["$count"] == "true"


def test_to_params_returns_copy():
    q = ODataQuery().top(5)
    p1 = q.to_params()
    p2 = q.to_params()
    p1["$top"] = 999
    assert p2["$top"] == 5


def test_repr():
    r = repr(ODataQuery().top(5))
    assert "$top" in r
