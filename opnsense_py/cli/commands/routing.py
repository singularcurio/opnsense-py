from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.routing import Gateway

routing_app = typer.Typer(name="routing", help="Manage gateway definitions.")


@routing_app.command("list")
@handle_api_errors
def gateway_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List gateways."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routing.search_gateways(SearchRequest(searchPhrase=search)), lctx.output_format))


@routing_app.command("get")
@handle_api_errors
def gateway_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a gateway by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routing.get_gateway(uuid), lctx.output_format))


@routing_app.command("add")
@handle_api_errors
def gateway_add(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(help="Gateway name.")],
    interface: Annotated[str, typer.Option()],
    gateway: Annotated[str | None, typer.Option(help="Gateway IP address.")] = None,
    ipprotocol: Annotated[str | None, typer.Option(help="inet or inet6")] = None,
    descr: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a gateway."""
    lctx = get_ctx(ctx)
    obj = build_model(Gateway, from_json, name=name, interface=interface,
                      gateway=gateway, ipprotocol=ipprotocol, descr=descr)
    typer.echo(render(lctx.client.routing.add_gateway(obj), lctx.output_format))


@routing_app.command("set")
@handle_api_errors
def gateway_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    name: Annotated[str | None, typer.Option()] = None,
    interface: Annotated[str | None, typer.Option()] = None,
    gateway: Annotated[str | None, typer.Option()] = None,
    ipprotocol: Annotated[str | None, typer.Option()] = None,
    descr: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a gateway."""
    lctx = get_ctx(ctx)
    obj = build_model(Gateway, from_json, name=name, interface=interface,
                      gateway=gateway, ipprotocol=ipprotocol, descr=descr)
    typer.echo(render(lctx.client.routing.set_gateway(uuid, obj), lctx.output_format))


@routing_app.command("del")
@handle_api_errors
def gateway_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a gateway."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routing.del_gateway(uuid), lctx.output_format))


@routing_app.command("toggle")
@handle_api_errors
def gateway_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a gateway on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routing.toggle_gateway(uuid, enabled=enable), lctx.output_format))


@routing_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply routing configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routing.reconfigure(), lctx.output_format))
