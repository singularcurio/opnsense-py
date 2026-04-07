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
