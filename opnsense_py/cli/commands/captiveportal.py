from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.models.base import SearchRequest

captiveportal_app = typer.Typer(name="captiveportal", help="Manage captive portal zones, sessions, and vouchers.")


# ===========================================================================
# Zones
# ===========================================================================

zone_app = typer.Typer(name="zone", help="Manage captive portal zones.")
captiveportal_app.add_typer(zone_app)


@zone_app.command("list")
@handle_api_errors
def zone_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List captive portal zones."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.search_zones(SearchRequest(searchPhrase=search)), lctx.output_format))


@zone_app.command("get")
@handle_api_errors
def zone_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a zone by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.get_zone(uuid), lctx.output_format))


@zone_app.command("del")
@handle_api_errors
def zone_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a zone."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.del_zone(uuid), lctx.output_format))


@zone_app.command("toggle")
@handle_api_errors
def zone_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a zone on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.toggle_zone(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Sessions
# ===========================================================================


@captiveportal_app.command("sessions")
@handle_api_errors
def sessions(ctx: typer.Context) -> None:
    """List active captive portal sessions."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.search_sessions(), lctx.output_format))


@captiveportal_app.command("disconnect")
@handle_api_errors
def disconnect(
    ctx: typer.Context,
    zone_id: Annotated[str, typer.Argument()],
) -> None:
    """Disconnect all sessions in a zone."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.disconnect_session(zone_id=zone_id), lctx.output_format))


# ===========================================================================
# Vouchers
# ===========================================================================

voucher_app = typer.Typer(name="voucher", help="Manage captive portal vouchers.")
captiveportal_app.add_typer(voucher_app)


@voucher_app.command("providers")
@handle_api_errors
def voucher_providers(ctx: typer.Context) -> None:
    """List voucher providers."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.list_voucher_providers(), lctx.output_format))


@voucher_app.command("groups")
@handle_api_errors
def voucher_groups(
    ctx: typer.Context,
    provider: Annotated[str, typer.Argument()],
) -> None:
    """List voucher groups for a provider."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.list_voucher_groups(provider), lctx.output_format))


@voucher_app.command("list")
@handle_api_errors
def voucher_list(
    ctx: typer.Context,
    provider: Annotated[str, typer.Argument()],
    group: Annotated[str, typer.Argument()],
) -> None:
    """List vouchers in a group."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.list_vouchers(provider, group), lctx.output_format))


@voucher_app.command("drop-group")
@handle_api_errors
def voucher_drop_group(
    ctx: typer.Context,
    provider: Annotated[str, typer.Argument()],
    group: Annotated[str, typer.Argument()],
) -> None:
    """Drop an entire voucher group."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.drop_voucher_group(provider, group), lctx.output_format))


@voucher_app.command("drop-expired")
@handle_api_errors
def voucher_drop_expired(
    ctx: typer.Context,
    provider: Annotated[str, typer.Argument()],
    group: Annotated[str, typer.Argument()],
) -> None:
    """Drop expired vouchers from a group."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.drop_expired_vouchers(provider, group), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@captiveportal_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show captive portal service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.status(), lctx.output_format))


@captiveportal_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply captive portal configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.reconfigure(), lctx.output_format))


@captiveportal_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the captive portal service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.start(), lctx.output_format))


@captiveportal_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the captive portal service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.stop(), lctx.output_format))


@captiveportal_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the captive portal service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.captiveportal.restart(), lctx.output_format))
