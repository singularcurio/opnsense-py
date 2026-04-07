from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.monit import MonitAlert, MonitService, MonitTest

monit_app = typer.Typer(name="monit", help="Manage Monit service checks, tests, and alerts.")


# ===========================================================================
# Services
# ===========================================================================

service_app = typer.Typer(name="service", help="Manage Monit service checks.")
monit_app.add_typer(service_app)


@service_app.command("list")
@handle_api_errors
def service_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List Monit service checks."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.search_services(SearchRequest(searchPhrase=search)), lctx.output_format))


@service_app.command("get")
@handle_api_errors
def service_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a Monit service check by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.get_service(uuid), lctx.output_format))


@service_app.command("add")
@handle_api_errors
def service_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type", help="Service type (process, host, etc.)")] = None,
    address: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a Monit service check."""
    lctx = get_ctx(ctx)
    obj = build_model(MonitService, from_json, name=name, type=type_, address=address,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.monit.add_service(obj), lctx.output_format))


@service_app.command("set")
@handle_api_errors
def service_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    name: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type")] = None,
    address: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a Monit service check."""
    lctx = get_ctx(ctx)
    obj = build_model(MonitService, from_json, name=name, type=type_, address=address,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.monit.set_service(uuid, obj), lctx.output_format))


@service_app.command("del")
@handle_api_errors
def service_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a Monit service check."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.del_service(uuid), lctx.output_format))


@service_app.command("toggle")
@handle_api_errors
def service_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a Monit service check."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.toggle_service(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Tests
# ===========================================================================

test_app = typer.Typer(name="test", help="Manage Monit test conditions.")
monit_app.add_typer(test_app)


@test_app.command("list")
@handle_api_errors
def test_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List Monit test conditions."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.search_tests(SearchRequest(searchPhrase=search)), lctx.output_format))


@test_app.command("get")
@handle_api_errors
def test_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a Monit test by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.get_test(uuid), lctx.output_format))


@test_app.command("add")
@handle_api_errors
def test_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type")] = None,
    condition: Annotated[str | None, typer.Option()] = None,
    action: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a Monit test condition."""
    lctx = get_ctx(ctx)
    obj = build_model(MonitTest, from_json, name=name, type=type_,
                      condition=condition, action=action)
    typer.echo(render(lctx.client.monit.add_test(obj), lctx.output_format))


@test_app.command("del")
@handle_api_errors
def test_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a Monit test condition."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.del_test(uuid), lctx.output_format))


# ===========================================================================
# Alerts
# ===========================================================================

alert_app = typer.Typer(name="alert", help="Manage Monit email alerts.")
monit_app.add_typer(alert_app)


@alert_app.command("list")
@handle_api_errors
def alert_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List Monit alerts."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.search_alerts(SearchRequest(searchPhrase=search)), lctx.output_format))


@alert_app.command("get")
@handle_api_errors
def alert_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a Monit alert by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.get_alert(uuid), lctx.output_format))


@alert_app.command("add")
@handle_api_errors
def alert_add(
    ctx: typer.Context,
    recipient: Annotated[str | None, typer.Option(help="Email recipient address.")] = None,
    events: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a Monit alert."""
    lctx = get_ctx(ctx)
    obj = build_model(MonitAlert, from_json, recipient=recipient, events=events,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.monit.add_alert(obj), lctx.output_format))


@alert_app.command("del")
@handle_api_errors
def alert_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a Monit alert."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.del_alert(uuid), lctx.output_format))


@alert_app.command("toggle")
@handle_api_errors
def alert_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a Monit alert."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.toggle_alert(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@monit_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show Monit service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.status(), lctx.output_format))


@monit_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply Monit configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.reconfigure(), lctx.output_format))


@monit_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the Monit service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.start(), lctx.output_format))


@monit_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the Monit service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.stop(), lctx.output_format))


@monit_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the Monit service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.monit.restart(), lctx.output_format))
