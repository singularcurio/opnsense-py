from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.dhcrelay import DHCRelayDestination, DHCRelayRelay

dhcrelay_app = typer.Typer(name="dhcrelay", help="Manage DHCP relay destinations and relays.")


# ===========================================================================
# Destinations
# ===========================================================================

destination_app = typer.Typer(name="destination", help="Manage DHCP relay destination servers.")
dhcrelay_app.add_typer(destination_app)


@destination_app.command("list")
@handle_api_errors
def destination_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List relay destinations."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.search_destinations(SearchRequest(searchPhrase=search)), lctx.output_format))


@destination_app.command("get")
@handle_api_errors
def destination_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a relay destination by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.get_destination(uuid), lctx.output_format))


@destination_app.command("add")
@handle_api_errors
def destination_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    server: Annotated[str | None, typer.Option(help="Destination server IP.")] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a relay destination."""
    lctx = get_ctx(ctx)
    obj = build_model(DHCRelayDestination, from_json, name=name, server=server)
    typer.echo(render(lctx.client.dhcrelay.add_destination(obj), lctx.output_format))


@destination_app.command("set")
@handle_api_errors
def destination_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    name: Annotated[str | None, typer.Option()] = None,
    server: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a relay destination."""
    lctx = get_ctx(ctx)
    obj = build_model(DHCRelayDestination, from_json, name=name, server=server)
    typer.echo(render(lctx.client.dhcrelay.set_destination(uuid, obj), lctx.output_format))


@destination_app.command("del")
@handle_api_errors
def destination_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a relay destination."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.del_destination(uuid), lctx.output_format))


# ===========================================================================
# Relays
# ===========================================================================

relay_app = typer.Typer(name="relay", help="Manage DHCP relay interface bindings.")
dhcrelay_app.add_typer(relay_app)


@relay_app.command("list")
@handle_api_errors
def relay_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List relays."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.search_relays(SearchRequest(searchPhrase=search)), lctx.output_format))


@relay_app.command("get")
@handle_api_errors
def relay_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a relay by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.get_relay(uuid), lctx.output_format))


@relay_app.command("add")
@handle_api_errors
def relay_add(
    ctx: typer.Context,
    interface: Annotated[str | None, typer.Option(help="Listening interface.")] = None,
    destination: Annotated[str | None, typer.Option(help="Destination UUID.")] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a relay."""
    lctx = get_ctx(ctx)
    obj = build_model(DHCRelayRelay, from_json, interface=interface, destination=destination, enabled=enabled)
    typer.echo(render(lctx.client.dhcrelay.add_relay(obj), lctx.output_format))


@relay_app.command("set")
@handle_api_errors
def relay_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    interface: Annotated[str | None, typer.Option()] = None,
    destination: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a relay."""
    lctx = get_ctx(ctx)
    obj = build_model(DHCRelayRelay, from_json, interface=interface, destination=destination, enabled=enabled)
    typer.echo(render(lctx.client.dhcrelay.set_relay(uuid, obj), lctx.output_format))


@relay_app.command("del")
@handle_api_errors
def relay_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a relay."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.del_relay(uuid), lctx.output_format))


@relay_app.command("toggle")
@handle_api_errors
def relay_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a relay on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.toggle_relay(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@dhcrelay_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply DHCP relay configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dhcrelay.reconfigure(), lctx.output_format))
