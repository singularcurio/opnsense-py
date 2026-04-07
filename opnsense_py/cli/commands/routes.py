from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.routes import Route

routes_app = typer.Typer(name="routes", help="Manage static routes and gateway status.")


@routes_app.command("list")
@handle_api_errors
def routes_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List static routes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routes.search_routes(SearchRequest(searchPhrase=search)), lctx.output_format))


@routes_app.command("get")
@handle_api_errors
def routes_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a static route by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routes.get_route(uuid), lctx.output_format))


@routes_app.command("add")
@handle_api_errors
def routes_add(
    ctx: typer.Context,
    network: Annotated[str, typer.Option(help="Destination network, e.g. 192.168.10.0/24.")],
    gateway: Annotated[str, typer.Option(help="Gateway name or IP.")],
    descr: Annotated[str | None, typer.Option(help="Description.")] = None,
    disabled: Annotated[str | None, typer.Option(help='"1" to disable the route.')] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a static route."""
    lctx = get_ctx(ctx)
    obj = build_model(Route, from_json, network=network, gateway=gateway,
                      descr=descr, disabled=disabled)
    typer.echo(render(lctx.client.routes.add_route(obj), lctx.output_format))


@routes_app.command("set")
@handle_api_errors
def routes_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    network: Annotated[str | None, typer.Option()] = None,
    gateway: Annotated[str | None, typer.Option()] = None,
    descr: Annotated[str | None, typer.Option()] = None,
    disabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a static route."""
    lctx = get_ctx(ctx)
    obj = build_model(Route, from_json, network=network, gateway=gateway,
                      descr=descr, disabled=disabled)
    typer.echo(render(lctx.client.routes.set_route(uuid, obj), lctx.output_format))


@routes_app.command("del")
@handle_api_errors
def routes_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a static route."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routes.del_route(uuid), lctx.output_format))


@routes_app.command("toggle")
@handle_api_errors
def routes_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a static route on or off."""
    lctx = get_ctx(ctx)
    # API uses disabled=True to disable, disabled=False to enable
    disabled = (not enable) if enable is not None else None
    typer.echo(render(lctx.client.routes.toggle_route(uuid, disabled=disabled), lctx.output_format))


@routes_app.command("gateways")
@handle_api_errors
def gateways(ctx: typer.Context) -> None:
    """Show gateway status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routes.gateway_status(), lctx.output_format))


@routes_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply route configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.routes.reconfigure(), lctx.output_format))
