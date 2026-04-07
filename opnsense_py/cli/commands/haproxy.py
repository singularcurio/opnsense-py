from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.models.base import SearchRequest

haproxy_app = typer.Typer(name="haproxy", help="Manage HAProxy frontends, backends, servers, and service.")


# ===========================================================================
# Frontends
# ===========================================================================

frontend_app = typer.Typer(name="frontend", help="Manage HAProxy frontends.")
haproxy_app.add_typer(frontend_app)


@frontend_app.command("list")
@handle_api_errors
def frontend_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List frontends."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.search_frontends(SearchRequest(searchPhrase=search)), lctx.output_format))


@frontend_app.command("get")
@handle_api_errors
def frontend_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a frontend by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.get_frontend(uuid), lctx.output_format))


@frontend_app.command("del")
@handle_api_errors
def frontend_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a frontend."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.del_frontend(uuid), lctx.output_format))


@frontend_app.command("toggle")
@handle_api_errors
def frontend_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Toggle a frontend on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.toggle_frontend(uuid), lctx.output_format))


# ===========================================================================
# Backends
# ===========================================================================

backend_app = typer.Typer(name="backend", help="Manage HAProxy backends.")
haproxy_app.add_typer(backend_app)


@backend_app.command("list")
@handle_api_errors
def backend_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List backends."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.search_backends(SearchRequest(searchPhrase=search)), lctx.output_format))


@backend_app.command("get")
@handle_api_errors
def backend_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a backend by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.get_backend(uuid), lctx.output_format))


@backend_app.command("del")
@handle_api_errors
def backend_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a backend."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.del_backend(uuid), lctx.output_format))


@backend_app.command("toggle")
@handle_api_errors
def backend_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a backend on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.toggle_backend(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Servers
# ===========================================================================

server_app = typer.Typer(name="server", help="Manage HAProxy servers.")
haproxy_app.add_typer(server_app)


@server_app.command("list")
@handle_api_errors
def server_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List servers."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.search_servers(SearchRequest(searchPhrase=search)), lctx.output_format))


@server_app.command("get")
@handle_api_errors
def server_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a server by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.get_server(uuid), lctx.output_format))


@server_app.command("del")
@handle_api_errors
def server_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a server."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.del_server(uuid), lctx.output_format))


@server_app.command("toggle")
@handle_api_errors
def server_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a server on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.toggle_server(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Statistics
# ===========================================================================


@haproxy_app.command("stats")
@handle_api_errors
def stats(ctx: typer.Context) -> None:
    """Show HAProxy statistics counters."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.stat_counters(), lctx.output_format))


@haproxy_app.command("info")
@handle_api_errors
def info(ctx: typer.Context) -> None:
    """Show HAProxy process info."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.stat_info(), lctx.output_format))


@haproxy_app.command("configtest")
@handle_api_errors
def configtest(ctx: typer.Context) -> None:
    """Test HAProxy configuration."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.configtest(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@haproxy_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show HAProxy service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.status(), lctx.output_format))


@haproxy_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply HAProxy configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.reconfigure(), lctx.output_format))


@haproxy_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the HAProxy service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.start(), lctx.output_format))


@haproxy_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the HAProxy service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.stop(), lctx.output_format))


@haproxy_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the HAProxy service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.haproxy.restart(), lctx.output_format))
