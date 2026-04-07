from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.syslog import SyslogDestination

syslog_app = typer.Typer(name="syslog", help="Manage remote syslog destinations.")


# ===========================================================================
# Destinations
# ===========================================================================


@syslog_app.command("list")
@handle_api_errors
def dest_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List syslog destinations."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.search_destinations(SearchRequest(searchPhrase=search)), lctx.output_format))


@syslog_app.command("get")
@handle_api_errors
def dest_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a syslog destination by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.get_destination(uuid), lctx.output_format))


@syslog_app.command("add")
@handle_api_errors
def dest_add(
    ctx: typer.Context,
    hostname: Annotated[str | None, typer.Option(help="Remote syslog server hostname.")] = None,
    port: Annotated[str | None, typer.Option()] = None,
    transport: Annotated[str | None, typer.Option(help="udp4, tcp4, tls4, etc.")] = None,
    level: Annotated[str | None, typer.Option()] = None,
    facility: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a syslog destination."""
    lctx = get_ctx(ctx)
    obj = build_model(SyslogDestination, from_json, hostname=hostname, port=port,
                      transport=transport, level=level, facility=facility,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.syslog.add_destination(obj), lctx.output_format))


@syslog_app.command("set")
@handle_api_errors
def dest_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    hostname: Annotated[str | None, typer.Option()] = None,
    port: Annotated[str | None, typer.Option()] = None,
    transport: Annotated[str | None, typer.Option()] = None,
    level: Annotated[str | None, typer.Option()] = None,
    facility: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a syslog destination."""
    lctx = get_ctx(ctx)
    obj = build_model(SyslogDestination, from_json, hostname=hostname, port=port,
                      transport=transport, level=level, facility=facility,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.syslog.set_destination(uuid, obj), lctx.output_format))


@syslog_app.command("del")
@handle_api_errors
def dest_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a syslog destination."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.del_destination(uuid), lctx.output_format))


@syslog_app.command("toggle")
@handle_api_errors
def dest_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a syslog destination."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.toggle_destination(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@syslog_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show syslog service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.status(), lctx.output_format))


@syslog_app.command("stats")
@handle_api_errors
def stats(ctx: typer.Context) -> None:
    """Show syslog statistics."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.stats(), lctx.output_format))


@syslog_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply syslog configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.reconfigure(), lctx.output_format))


@syslog_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the syslog service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.start(), lctx.output_format))


@syslog_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the syslog service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.stop(), lctx.output_format))


@syslog_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the syslog service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.syslog.restart(), lctx.output_format))
