from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.ids import IDSPolicy, IDSUserRule

ids_app = typer.Typer(name="ids", help="Manage IDS/IPS (Suricata) policies, rules, and alerts.")


# ===========================================================================
# Policies
# ===========================================================================

policy_app = typer.Typer(name="policy", help="Manage IDS policies.")
ids_app.add_typer(policy_app)


@policy_app.command("list")
@handle_api_errors
def policy_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List IDS policies."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.search_policies(SearchRequest(searchPhrase=search)), lctx.output_format))


@policy_app.command("get")
@handle_api_errors
def policy_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get an IDS policy by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.get_policy(uuid), lctx.output_format))


@policy_app.command("add")
@handle_api_errors
def policy_add(
    ctx: typer.Context,
    description: Annotated[str | None, typer.Option()] = None,
    action: Annotated[str | None, typer.Option(help="alert, drop, or pass")] = None,
    rulesets: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add an IDS policy."""
    lctx = get_ctx(ctx)
    obj = build_model(IDSPolicy, from_json, description=description, action=action,
                      rulesets=rulesets, enabled=enabled)
    typer.echo(render(lctx.client.ids.add_policy(obj), lctx.output_format))


@policy_app.command("del")
@handle_api_errors
def policy_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete an IDS policy."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.del_policy(uuid), lctx.output_format))


@policy_app.command("toggle")
@handle_api_errors
def policy_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle an IDS policy."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.toggle_policy(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# User rules
# ===========================================================================

rule_app = typer.Typer(name="rule", help="Manage custom IDS user rules.")
ids_app.add_typer(rule_app)


@rule_app.command("list")
@handle_api_errors
def rule_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List user-defined IDS rules."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.search_user_rules(SearchRequest(searchPhrase=search)), lctx.output_format))


@rule_app.command("get")
@handle_api_errors
def rule_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a user rule by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.get_user_rule(uuid), lctx.output_format))


@rule_app.command("add")
@handle_api_errors
def rule_add(
    ctx: typer.Context,
    source: Annotated[str | None, typer.Option()] = None,
    destination: Annotated[str | None, typer.Option()] = None,
    action: Annotated[str | None, typer.Option(help="alert, drop, or pass")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a user-defined IDS rule."""
    lctx = get_ctx(ctx)
    obj = build_model(IDSUserRule, from_json, source=source, destination=destination,
                      action=action, description=description, enabled=enabled)
    typer.echo(render(lctx.client.ids.add_user_rule(obj), lctx.output_format))


@rule_app.command("del")
@handle_api_errors
def rule_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a user rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.del_user_rule(uuid), lctx.output_format))


@rule_app.command("toggle")
@handle_api_errors
def rule_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a user rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.toggle_user_rule(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Rulesets
# ===========================================================================


@ids_app.command("rulesets")
@handle_api_errors
def rulesets(ctx: typer.Context) -> None:
    """List available IDS rulesets."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.list_rulesets(), lctx.output_format))


@ids_app.command("update-rules")
@handle_api_errors
def update_rules(ctx: typer.Context) -> None:
    """Download and update IDS rules from configured sources."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.update_rules(), lctx.output_format))


# ===========================================================================
# Alerts
# ===========================================================================


@ids_app.command("alerts")
@handle_api_errors
def alerts(ctx: typer.Context) -> None:
    """Show recent IDS alert log entries."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.get_alert_logs(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@ids_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show IDS service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.status(), lctx.output_format))


@ids_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply IDS configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.reconfigure(), lctx.output_format))


@ids_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the IDS service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.start(), lctx.output_format))


@ids_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the IDS service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.stop(), lctx.output_format))


@ids_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the IDS service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ids.restart(), lctx.output_format))
