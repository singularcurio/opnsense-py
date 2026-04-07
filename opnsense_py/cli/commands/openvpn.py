from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.openvpn import OpenVPNInstance, OpenVPNOverwrite

openvpn_app = typer.Typer(name="openvpn", help="Manage OpenVPN instances, overwrites, and sessions.")


# ===========================================================================
# Instances
# ===========================================================================

instance_app = typer.Typer(name="instance", help="Manage OpenVPN server/client instances.")
openvpn_app.add_typer(instance_app)


@instance_app.command("list")
@handle_api_errors
def instance_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List OpenVPN instances."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.search_instances(SearchRequest(searchPhrase=search)), lctx.output_format))


@instance_app.command("get")
@handle_api_errors
def instance_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get an OpenVPN instance by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.get_instance(uuid), lctx.output_format))


@instance_app.command("add")
@handle_api_errors
def instance_add(
    ctx: typer.Context,
    role: Annotated[str | None, typer.Option(help="server or client")] = None,
    proto: Annotated[str | None, typer.Option(help="udp, tcp-server, tcp-client")] = None,
    port: Annotated[str | None, typer.Option()] = None,
    server: Annotated[str | None, typer.Option(help="Server network, e.g. 10.8.0.0/24")] = None,
    remote: Annotated[str | None, typer.Option(help="Remote host (client mode).")] = None,
    cert: Annotated[str | None, typer.Option(help="Certificate UUID.")] = None,
    ca: Annotated[str | None, typer.Option(help="CA UUID.")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add an OpenVPN instance."""
    lctx = get_ctx(ctx)
    obj = build_model(OpenVPNInstance, from_json, role=role, proto=proto, port=port,
                      server=server, remote=remote, cert=cert, ca=ca,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.openvpn.add_instance(obj), lctx.output_format))


@instance_app.command("set")
@handle_api_errors
def instance_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    role: Annotated[str | None, typer.Option()] = None,
    proto: Annotated[str | None, typer.Option()] = None,
    port: Annotated[str | None, typer.Option()] = None,
    server: Annotated[str | None, typer.Option()] = None,
    remote: Annotated[str | None, typer.Option()] = None,
    cert: Annotated[str | None, typer.Option()] = None,
    ca: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update an OpenVPN instance."""
    lctx = get_ctx(ctx)
    obj = build_model(OpenVPNInstance, from_json, role=role, proto=proto, port=port,
                      server=server, remote=remote, cert=cert, ca=ca,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.openvpn.set_instance(uuid, obj), lctx.output_format))


@instance_app.command("del")
@handle_api_errors
def instance_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete an OpenVPN instance."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.del_instance(uuid), lctx.output_format))


@instance_app.command("toggle")
@handle_api_errors
def instance_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle an OpenVPN instance on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.toggle_instance(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Client overwrites
# ===========================================================================

overwrite_app = typer.Typer(name="overwrite", help="Manage OpenVPN client-specific configuration overwrites.")
openvpn_app.add_typer(overwrite_app)


@overwrite_app.command("list")
@handle_api_errors
def overwrite_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List client overwrites."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.search_client_overwrites(SearchRequest(searchPhrase=search)), lctx.output_format))


@overwrite_app.command("get")
@handle_api_errors
def overwrite_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a client overwrite by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.get_client_overwrite(uuid), lctx.output_format))


@overwrite_app.command("add")
@handle_api_errors
def overwrite_add(
    ctx: typer.Context,
    common_name: Annotated[str | None, typer.Option("--common-name")] = None,
    servers: Annotated[str | None, typer.Option(help="Comma-separated server UUIDs.")] = None,
    tunnel_network: Annotated[str | None, typer.Option("--tunnel-network")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a client overwrite."""
    lctx = get_ctx(ctx)
    obj = build_model(OpenVPNOverwrite, from_json, common_name=common_name, servers=servers,
                      tunnel_network=tunnel_network, description=description, enabled=enabled)
    typer.echo(render(lctx.client.openvpn.add_client_overwrite(obj), lctx.output_format))


@overwrite_app.command("del")
@handle_api_errors
def overwrite_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a client overwrite."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.del_client_overwrite(uuid), lctx.output_format))


# ===========================================================================
# Sessions
# ===========================================================================


@openvpn_app.command("sessions")
@handle_api_errors
def sessions(ctx: typer.Context) -> None:
    """List active OpenVPN sessions."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.search_sessions(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@openvpn_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply OpenVPN configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.reconfigure(), lctx.output_format))


@openvpn_app.command("start")
@handle_api_errors
def start(
    ctx: typer.Context,
    service_id: Annotated[str | None, typer.Option("--id", help="Instance UUID (omit for all).")] = None,
) -> None:
    """Start OpenVPN service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.start_service(service_id), lctx.output_format))


@openvpn_app.command("stop")
@handle_api_errors
def stop(
    ctx: typer.Context,
    service_id: Annotated[str | None, typer.Option("--id", help="Instance UUID (omit for all).")] = None,
) -> None:
    """Stop OpenVPN service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.stop_service(service_id), lctx.output_format))


@openvpn_app.command("restart")
@handle_api_errors
def restart(
    ctx: typer.Context,
    service_id: Annotated[str | None, typer.Option("--id", help="Instance UUID (omit for all).")] = None,
) -> None:
    """Restart OpenVPN service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.openvpn.restart_service(service_id), lctx.output_format))
