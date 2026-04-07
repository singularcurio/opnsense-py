import httpx
import pytest
import respx

from opnsense_py import OPNsenseClient
from opnsense_py.models.firewall import (
    FilterRule,
    FirewallAlias,
    NPTRule,
    OneToOneRule,
    SNatRule,
)


def test_savepoint_yields_revision(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/firewall/filter/savepoint").mock(
        return_value=httpx.Response(200, json={"revision": "1711234567.123"})
    )
    with client.firewall.savepoint("filter") as revision:
        assert revision == "1711234567.123"


def test_savepoint_does_not_cancel_on_exception(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/firewall/filter/savepoint").mock(
        return_value=httpx.Response(200, json={"revision": "abc"})
    )
    cancel_route = mock_api.post("/api/firewall/filter/cancel_rollback/abc")

    with pytest.raises(RuntimeError):
        with client.firewall.savepoint("filter"):
            raise RuntimeError("test error")

    assert not cancel_route.called


def test_cancel_rollback(client: OPNsenseClient, mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/firewall/filter/cancel_rollback/rev-123").mock(
        return_value=httpx.Response(200, json={"result": "ok"})
    )
    client.firewall.cancel_rollback("rev-123")
    assert route.called


def test_apply_with_revision(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/firewall/filter/apply/rev-123").mock(
        return_value=httpx.Response(200, json={"result": "ok"})
    )
    client.firewall.apply("rev-123")
    assert route.called


def test_apply_without_revision(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/firewall/filter/apply").mock(
        return_value=httpx.Response(200, json={"result": "ok"})
    )
    client.firewall.apply()
    assert route.called


def test_search_filter_rules(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/firewall/filter/search_rule").mock(
        return_value=httpx.Response(
            200,
            json={
                "total": 1,
                "rowCount": 1,
                "current": 1,
                "rows": [{"uuid": "rule-uuid", "description": "test rule"}],
            },
        )
    )
    result = client.firewall.search_filter_rules()
    assert result.total == 1
    assert result.rows[0].uuid == "rule-uuid"


def test_toggle_filter_rule_enabled(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/firewall/filter/toggle_rule/rule-uuid/1").mock(
        return_value=httpx.Response(200, json={"result": "saved"})
    )
    client.firewall.toggle_filter_rule("rule-uuid", enabled=True)
    assert route.called


@pytest.mark.parametrize(
    "model_cls",
    [FilterRule, FirewallAlias, SNatRule, NPTRule, OneToOneRule],
)
def test_categories_empty_list_coerced_to_empty_string(model_cls: type) -> None:
    """OPNsense returns categories: [] for resources with no category assigned."""
    instance = model_cls.model_validate({"categories": []})
    assert instance.categories == ""


@pytest.mark.parametrize(
    "model_cls",
    [FilterRule, FirewallAlias, SNatRule, NPTRule, OneToOneRule],
)
def test_categories_string_value_unchanged(model_cls: type) -> None:
    instance = model_cls.model_validate({"categories": "some-uuid"})
    assert instance.categories == "some-uuid"


def test_get_alias_parses_edit_form_response(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    """get_alias must parse the form-data format returned by getAlias/{uuid}."""
    mock_api.get("/api/firewall/alias/get_item/alias-uuid").mock(
        return_value=httpx.Response(
            200,
            json={
                "alias": {
                    "enabled": "1",
                    "name": "my_alias",
                    "type": {
                        "host": {"value": "Host(s)", "selected": 0},
                        "network": {"value": "Network(s)", "selected": 1},
                        "port": {"value": "Port(s)", "selected": 0},
                    },
                    "proto": {
                        "": {"value": "any", "selected": 1},
                        "IPv4": {"value": "IPv4", "selected": 0},
                        "IPv6": {"value": "IPv6", "selected": 0},
                    },
                    "interface": {
                        "": {"value": "any", "selected": 1},
                        "wan": {"value": "WAN", "selected": 0},
                    },
                    "content": {
                        "192.168.1.0/24": {"value": "192.168.1.0/24", "selected": 1},
                        "10.0.0.0/8": {"value": "10.0.0.0/8", "selected": 1},
                    },
                    "categories": [],
                    "description": "Test alias",
                }
            },
        )
    )
    alias = client.firewall.get_alias("alias-uuid")
    assert alias.type == "network"
    assert alias.proto == ""
    assert alias.interface == ""
    assert alias.content == "192.168.1.0/24\n10.0.0.0/8"
    assert alias.categories == ""
    assert alias.description == "Test alias"


def test_get_alias_single_content_entry(
    client: OPNsenseClient, mock_api: respx.MockRouter
) -> None:
    mock_api.get("/api/firewall/alias/get_item/alias-uuid").mock(
        return_value=httpx.Response(
            200,
            json={
                "alias": {
                    "name": "single",
                    "type": {
                        "host": {"value": "Host(s)", "selected": 1},
                    },
                    "content": {
                        "192.30.252.0/22": {"value": "192.30.252.0/22", "selected": 1},
                    },
                    "categories": [],
                }
            },
        )
    )
    alias = client.firewall.get_alias("alias-uuid")
    assert alias.type == "host"
    assert alias.content == "192.30.252.0/22"


def test_search_aliases(client: OPNsenseClient, mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/firewall/alias/search_item").mock(
        return_value=httpx.Response(
            200,
            json={
                "total": 2,
                "rowCount": 2,
                "current": 1,
                "rows": [{"uuid": "a1"}, {"uuid": "a2"}],
            },
        )
    )
    result = client.firewall.search_aliases()
    assert result.total == 2
