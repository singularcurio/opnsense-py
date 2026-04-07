from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.ipsec import IPsecChild, IPsecConnection

ipsec_app = typer.Typer(name="ipsec", help="Manage IPsec VPN connections.")


# ===========================================================================
# Connections
# ===========================================================================

connection_app = typer.Typer(name="connection", help="Manage IPsec IKE connections.")
ipsec_app.add_typer(connection_app)


@connection_app.command("list")
@handle_api_errors
def connection_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List IPsec connections."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.search_connections(SearchRequest(searchPhrase=search)), lctx.output_format))


@connection_app.command("get")
@handle_api_errors
def connection_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get an IPsec connection by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.get_connection(uuid), lctx.output_format))


@connection_app.command("add")
@handle_api_errors
def connection_add(
    ctx: typer.Context,
    local_addrs: Annotated[str | None, typer.Option("--local-addrs")] = None,
    remote_addrs: Annotated[str | None, typer.Option("--remote-addrs")] = None,
    version: Annotated[str | None, typer.Option(help="IKE version: 1 or 2")] = None,
    proposals: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add an IPsec connection."""
    lctx = get_ctx(ctx)
    obj = build_model(IPsecConnection, from_json, local_addrs=local_addrs,
                      remote_addrs=remote_addrs, version=version, proposals=proposals,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.ipsec.add_connection(obj), lctx.output_format))


@connection_app.command("set")
@handle_api_errors
def connection_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    local_addrs: Annotated[str | None, typer.Option("--local-addrs")] = None,
    remote_addrs: Annotated[str | None, typer.Option("--remote-addrs")] = None,
    version: Annotated[str | None, typer.Option()] = None,
    proposals: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update an IPsec connection."""
    lctx = get_ctx(ctx)
    obj = build_model(IPsecConnection, from_json, local_addrs=local_addrs,
                      remote_addrs=remote_addrs, version=version, proposals=proposals,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.ipsec.set_connection(uuid, obj), lctx.output_format))


@connection_app.command("del")
@handle_api_errors
def connection_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete an IPsec connection."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.del_connection(uuid), lctx.output_format))


@connection_app.command("toggle")
@handle_api_errors
def connection_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle an IPsec connection."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.toggle_connection(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Child SAs
# ===========================================================================

child_app = typer.Typer(name="child", help="Manage IPsec child SAs (tunnels).")
ipsec_app.add_typer(child_app)


@child_app.command("list")
@handle_api_errors
def child_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List IPsec child SAs."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.search_children(SearchRequest(searchPhrase=search)), lctx.output_format))


@child_app.command("get")
@handle_api_errors
def child_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get an IPsec child SA by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.get_child(uuid), lctx.output_format))


@child_app.command("add")
@handle_api_errors
def child_add(
    ctx: typer.Context,
    connection: Annotated[str | None, typer.Option(help="Parent connection UUID.")] = None,
    local_ts: Annotated[str | None, typer.Option("--local-ts", help="Local traffic selectors.")] = None,
    remote_ts: Annotated[str | None, typer.Option("--remote-ts", help="Remote traffic selectors.")] = None,
    mode: Annotated[str | None, typer.Option(help="tunnel or transport")] = None,
    esp_proposals: Annotated[str | None, typer.Option("--esp-proposals")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add an IPsec child SA."""
    lctx = get_ctx(ctx)
    obj = build_model(IPsecChild, from_json, connection=connection, local_ts=local_ts,
                      remote_ts=remote_ts, mode=mode, esp_proposals=esp_proposals,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.ipsec.add_child(obj), lctx.output_format))


@child_app.command("del")
@handle_api_errors
def child_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete an IPsec child SA."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.del_child(uuid), lctx.output_format))


@child_app.command("toggle")
@handle_api_errors
def child_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle an IPsec child SA."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.toggle_child(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Sessions
# ===========================================================================


@ipsec_app.command("sessions")
@handle_api_errors
def sessions(ctx: typer.Context) -> None:
    """Show active IPsec IKE sessions."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.search_sessions_phase1(), lctx.output_format))


@ipsec_app.command("leases")
@handle_api_errors
def leases(ctx: typer.Context) -> None:
    """Show IPsec address pool leases."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.search_leases(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@ipsec_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show IPsec service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.status(), lctx.output_format))


@ipsec_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply IPsec configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.reconfigure(), lctx.output_format))


@ipsec_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the IPsec service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.start(), lctx.output_format))


@ipsec_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the IPsec service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.stop(), lctx.output_format))


@ipsec_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the IPsec service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ipsec.restart(), lctx.output_format))
