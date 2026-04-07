from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.wireguard import WireguardPeer, WireguardServer

wireguard_app = typer.Typer(name="wireguard", help="Manage WireGuard VPN servers and peers.")


# ===========================================================================
# Servers
# ===========================================================================

server_app = typer.Typer(name="server", help="Manage WireGuard server instances.")
wireguard_app.add_typer(server_app)


@server_app.command("list")
@handle_api_errors
def server_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List WireGuard servers."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.search_servers(SearchRequest(searchPhrase=search)), lctx.output_format))


@server_app.command("get")
@handle_api_errors
def server_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a WireGuard server by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.get_server(uuid), lctx.output_format))


@server_app.command("add")
@handle_api_errors
def server_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    port: Annotated[str | None, typer.Option()] = None,
    tunneladdress: Annotated[str | None, typer.Option(help="Tunnel IP address(es), e.g. 10.0.0.1/24.")] = None,
    dns: Annotated[str | None, typer.Option()] = None,
    mtu: Annotated[int | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    peers: Annotated[str | None, typer.Option(help="Comma-separated peer UUIDs.")] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a WireGuard server."""
    lctx = get_ctx(ctx)
    obj = build_model(WireguardServer, from_json, name=name, port=port,
                      tunneladdress=tunneladdress, dns=dns, mtu=mtu,
                      enabled=enabled, peers=peers)
    typer.echo(render(lctx.client.wireguard.add_server(obj), lctx.output_format))


@server_app.command("set")
@handle_api_errors
def server_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    name: Annotated[str | None, typer.Option()] = None,
    port: Annotated[str | None, typer.Option()] = None,
    tunneladdress: Annotated[str | None, typer.Option()] = None,
    dns: Annotated[str | None, typer.Option()] = None,
    mtu: Annotated[int | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    peers: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a WireGuard server."""
    lctx = get_ctx(ctx)
    obj = build_model(WireguardServer, from_json, name=name, port=port,
                      tunneladdress=tunneladdress, dns=dns, mtu=mtu,
                      enabled=enabled, peers=peers)
    typer.echo(render(lctx.client.wireguard.set_server(uuid, obj), lctx.output_format))


@server_app.command("del")
@handle_api_errors
def server_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a WireGuard server."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.del_server(uuid), lctx.output_format))


@server_app.command("toggle")
@handle_api_errors
def server_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Toggle a WireGuard server on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.toggle_server(uuid), lctx.output_format))


@server_app.command("keygen")
@handle_api_errors
def server_keygen(ctx: typer.Context) -> None:
    """Generate a new WireGuard public/private key pair."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.key_pair(), lctx.output_format))


# ===========================================================================
# Peers
# ===========================================================================

peer_app = typer.Typer(name="peer", help="Manage WireGuard peers (clients).")
wireguard_app.add_typer(peer_app)


@peer_app.command("list")
@handle_api_errors
def peer_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List WireGuard peers."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.search_clients(SearchRequest(searchPhrase=search)), lctx.output_format))


@peer_app.command("get")
@handle_api_errors
def peer_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a WireGuard peer by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.get_client(uuid), lctx.output_format))


@peer_app.command("add")
@handle_api_errors
def peer_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    pubkey: Annotated[str | None, typer.Option(help="Peer public key.")] = None,
    tunneladdress: Annotated[str | None, typer.Option(help="Allowed IPs / tunnel address.")] = None,
    serveraddress: Annotated[str | None, typer.Option()] = None,
    serverport: Annotated[str | None, typer.Option()] = None,
    keepalive: Annotated[int | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a WireGuard peer."""
    lctx = get_ctx(ctx)
    obj = build_model(WireguardPeer, from_json, name=name, pubkey=pubkey,
                      tunneladdress=tunneladdress, serveraddress=serveraddress,
                      serverport=serverport, keepalive=keepalive, enabled=enabled)
    typer.echo(render(lctx.client.wireguard.add_client_builder(obj), lctx.output_format))


@peer_app.command("set")
@handle_api_errors
def peer_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    name: Annotated[str | None, typer.Option()] = None,
    pubkey: Annotated[str | None, typer.Option()] = None,
    tunneladdress: Annotated[str | None, typer.Option()] = None,
    serveraddress: Annotated[str | None, typer.Option()] = None,
    serverport: Annotated[str | None, typer.Option()] = None,
    keepalive: Annotated[int | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a WireGuard peer."""
    lctx = get_ctx(ctx)
    obj = build_model(WireguardPeer, from_json, name=name, pubkey=pubkey,
                      tunneladdress=tunneladdress, serveraddress=serveraddress,
                      serverport=serverport, keepalive=keepalive, enabled=enabled)
    typer.echo(render(lctx.client.wireguard.set_client(uuid, obj), lctx.output_format))


@peer_app.command("del")
@handle_api_errors
def peer_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a WireGuard peer."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.del_client(uuid), lctx.output_format))


@peer_app.command("toggle")
@handle_api_errors
def peer_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Toggle a WireGuard peer on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.toggle_client(uuid), lctx.output_format))


@peer_app.command("psk")
@handle_api_errors
def peer_psk(ctx: typer.Context) -> None:
    """Generate a new pre-shared key."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.psk(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@wireguard_app.command("show")
@handle_api_errors
def show(ctx: typer.Context) -> None:
    """Show live WireGuard interface status (wg show)."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.show(), lctx.output_format))


@wireguard_app.command("status")
@handle_api_errors
def wg_status(ctx: typer.Context) -> None:
    """Show WireGuard service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.status(), lctx.output_format))


@wireguard_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply WireGuard configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.reconfigure(), lctx.output_format))


@wireguard_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the WireGuard service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.start(), lctx.output_format))


@wireguard_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the WireGuard service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.stop(), lctx.output_format))


@wireguard_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the WireGuard service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.wireguard.restart(), lctx.output_format))
