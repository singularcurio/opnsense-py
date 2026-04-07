from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.kea import KeaHaPeer, KeaReservation4, KeaSubnet4

kea_app = typer.Typer(name="kea", help="Manage Kea DHCP subnets, reservations, and service.")


# ===========================================================================
# DHCPv4 Subnets
# ===========================================================================

subnet4_app = typer.Typer(name="subnet4", help="Manage Kea DHCPv4 subnets.")
kea_app.add_typer(subnet4_app)


@subnet4_app.command("list")
@handle_api_errors
def subnet4_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List DHCPv4 subnets."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.search_v4_subnets(SearchRequest(searchPhrase=search)), lctx.output_format))


@subnet4_app.command("get")
@handle_api_errors
def subnet4_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a DHCPv4 subnet by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.get_v4_subnet(uuid), lctx.output_format))


@subnet4_app.command("add")
@handle_api_errors
def subnet4_add(
    ctx: typer.Context,
    subnet: Annotated[str | None, typer.Option(help="Subnet CIDR, e.g. 192.168.1.0/24.")] = None,
    pools: Annotated[str | None, typer.Option(help="Address pool ranges.")] = None,
    next_server: Annotated[str | None, typer.Option("--next-server")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a DHCPv4 subnet."""
    lctx = get_ctx(ctx)
    obj = build_model(KeaSubnet4, from_json, subnet=subnet, pools=pools,
                      next_server=next_server, description=description)
    typer.echo(render(lctx.client.kea.add_v4_subnet(obj), lctx.output_format))


@subnet4_app.command("set")
@handle_api_errors
def subnet4_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    subnet: Annotated[str | None, typer.Option()] = None,
    pools: Annotated[str | None, typer.Option()] = None,
    next_server: Annotated[str | None, typer.Option("--next-server")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a DHCPv4 subnet."""
    lctx = get_ctx(ctx)
    obj = build_model(KeaSubnet4, from_json, subnet=subnet, pools=pools,
                      next_server=next_server, description=description)
    typer.echo(render(lctx.client.kea.set_v4_subnet(uuid, obj), lctx.output_format))


@subnet4_app.command("del")
@handle_api_errors
def subnet4_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a DHCPv4 subnet."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.del_v4_subnet(uuid), lctx.output_format))


# ===========================================================================
# DHCPv4 Reservations
# ===========================================================================

reservation4_app = typer.Typer(name="reservation4", help="Manage Kea DHCPv4 host reservations.")
kea_app.add_typer(reservation4_app)


@reservation4_app.command("list")
@handle_api_errors
def reservation4_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List DHCPv4 reservations."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.search_v4_reservations(SearchRequest(searchPhrase=search)), lctx.output_format))


@reservation4_app.command("get")
@handle_api_errors
def reservation4_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a DHCPv4 reservation by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.get_v4_reservation(uuid), lctx.output_format))


@reservation4_app.command("add")
@handle_api_errors
def reservation4_add(
    ctx: typer.Context,
    subnet: Annotated[str | None, typer.Option(help="Parent subnet UUID.")] = None,
    ip_address: Annotated[str | None, typer.Option("--ip-address")] = None,
    hw_address: Annotated[str | None, typer.Option("--hw-address", help="MAC address.")] = None,
    hostname: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a DHCPv4 reservation."""
    lctx = get_ctx(ctx)
    obj = build_model(KeaReservation4, from_json, subnet=subnet, ip_address=ip_address,
                      hw_address=hw_address, hostname=hostname, description=description)
    typer.echo(render(lctx.client.kea.add_v4_reservation(obj), lctx.output_format))


@reservation4_app.command("set")
@handle_api_errors
def reservation4_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    subnet: Annotated[str | None, typer.Option()] = None,
    ip_address: Annotated[str | None, typer.Option("--ip-address")] = None,
    hw_address: Annotated[str | None, typer.Option("--hw-address")] = None,
    hostname: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a DHCPv4 reservation."""
    lctx = get_ctx(ctx)
    obj = build_model(KeaReservation4, from_json, subnet=subnet, ip_address=ip_address,
                      hw_address=hw_address, hostname=hostname, description=description)
    typer.echo(render(lctx.client.kea.set_v4_reservation(uuid, obj), lctx.output_format))


@reservation4_app.command("del")
@handle_api_errors
def reservation4_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a DHCPv4 reservation."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.del_v4_reservation(uuid), lctx.output_format))


# ===========================================================================
# DHCPv4 HA Peers
# ===========================================================================

peer4_app = typer.Typer(name="peer4", help="Manage Kea DHCPv4 high-availability peers.")
kea_app.add_typer(peer4_app)


@peer4_app.command("list")
@handle_api_errors
def peer4_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List DHCPv4 HA peers."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.search_v4_peers(SearchRequest(searchPhrase=search)), lctx.output_format))


@peer4_app.command("get")
@handle_api_errors
def peer4_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a DHCPv4 HA peer by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.get_v4_peer(uuid), lctx.output_format))


@peer4_app.command("add")
@handle_api_errors
def peer4_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    role: Annotated[str | None, typer.Option(help="primary, secondary, or standby")] = None,
    url: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a DHCPv4 HA peer."""
    lctx = get_ctx(ctx)
    obj = build_model(KeaHaPeer, from_json, name=name, role=role, url=url)
    typer.echo(render(lctx.client.kea.add_v4_peer(obj), lctx.output_format))


@peer4_app.command("del")
@handle_api_errors
def peer4_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a DHCPv4 HA peer."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.del_v4_peer(uuid), lctx.output_format))


# ===========================================================================
# Leases
# ===========================================================================


@kea_app.command("leases")
@handle_api_errors
def leases(ctx: typer.Context) -> None:
    """Show active DHCP leases."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.search_leases(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@kea_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show Kea service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.status(), lctx.output_format))


@kea_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply Kea configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.reconfigure(), lctx.output_format))


@kea_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the Kea service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.start(), lctx.output_format))


@kea_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the Kea service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.stop(), lctx.output_format))


@kea_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the Kea service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.kea.restart(), lctx.output_format))
