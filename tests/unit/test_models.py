import pytest

from opnsense_py.models.base import ApiResponse, SearchRequest, SearchResponse
from opnsense_py.models.unbound import HostOverride, UnboundDnsbl


def test_search_request_defaults() -> None:
    req = SearchRequest()
    assert req.current == 1
    assert req.rowCount == 500
    assert req.searchPhrase == ""
    assert req.sort == {}


def test_search_response_parses() -> None:
    raw = {
        "total": 2,
        "rowCount": 2,
        "current": 1,
        "rows": [{"uuid": "a"}, {"uuid": "b"}],
    }
    resp = SearchResponse[dict].model_validate(raw)
    assert resp.total == 2
    assert len(resp.rows) == 2
    assert resp.rows[0]["uuid"] == "a"


def test_api_response_accepts_extra_fields() -> None:
    raw = {"result": "saved", "uuid": "abc", "extra_field": "ignored"}
    resp = ApiResponse.model_validate(raw)
    assert resp.result == "saved"
    assert resp.uuid == "abc"


def test_api_response_no_validations() -> None:
    resp = ApiResponse.model_validate({"result": "ok"})
    assert resp.validations is None


class TestHostOverrideEditFormNormalization:
    """HostOverride.model_validate handles the edit-form response shape."""

    def test_rr_dropdown_dict_extracts_selected(self) -> None:
        raw = {
            "hostname": "myhost",
            "domain": "example.com",
            "rr": {
                "A": {"value": "A (IPv4 address)", "selected": 1},
                "AAAA": {"value": "AAAA (IPv6 address)", "selected": 0},
                "MX": {"value": "MX (mail)", "selected": 0},
            },
        }
        host = HostOverride.model_validate(raw)
        assert host.rr == "A"

    def test_addptr_dropdown_dict_extracts_selected(self) -> None:
        raw = {
            "hostname": "myhost",
            "domain": "example.com",
            "addptr": {
                "0": {"value": "No", "selected": 0},
                "1": {"value": "Yes", "selected": 1},
            },
        }
        host = HostOverride.model_validate(raw)
        assert host.addptr == "1"

    def test_empty_string_mxprio_becomes_none(self) -> None:
        raw = {"hostname": "myhost", "domain": "example.com", "mxprio": ""}
        host = HostOverride.model_validate(raw)
        assert host.mxprio is None

    def test_empty_string_ttl_becomes_none(self) -> None:
        raw = {"hostname": "myhost", "domain": "example.com", "ttl": ""}
        host = HostOverride.model_validate(raw)
        assert host.ttl is None

    def test_integer_mxprio_and_ttl_pass_through(self) -> None:
        raw = {"hostname": "myhost", "domain": "example.com", "mxprio": 10, "ttl": 300}
        host = HostOverride.model_validate(raw)
        assert host.mxprio == 10
        assert host.ttl == 300

    def test_full_edit_form_response(self) -> None:
        """Mirrors the actual get_host_override payload shape that triggered the bug."""
        raw = {
            "hostname": "mail",
            "domain": "example.com",
            "rr": {
                "A": {"value": "A (IPv4 address)", "selected": 0},
                "AAAA": {"value": "AAAA (IPv6 address)", "selected": 0},
                "MX": {"value": "MX (mail)", "selected": 1},
            },
            "mxprio": "",
            "ttl": "",
            "server": "1.2.3.4",
            "addptr": {
                "0": {"value": "No", "selected": 1},
                "1": {"value": "Yes", "selected": 0},
            },
        }
        host = HostOverride.model_validate(raw)
        assert host.rr == "MX"
        assert host.mxprio is None
        assert host.ttl is None
        assert host.addptr == "0"

    def test_str_fields_not_coerced(self) -> None:
        # Empty string on a str | None field must be preserved so write payloads
        # (e.g. clearing a text field) are not silently dropped.
        host = HostOverride.model_validate({"hostname": "", "description": ""})
        assert host.hostname == ""
        assert host.description == ""


def test_unbound_dnsbl_empty_cache_ttl() -> None:
    dnsbl = UnboundDnsbl.model_validate({"cache_ttl": ""})
    assert dnsbl.cache_ttl is None
