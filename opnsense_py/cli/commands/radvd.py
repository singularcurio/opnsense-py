from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.models.base import SearchRequest

radvd_app = typer.Typer(name="radvd", help="Manage Router Advertisement daemon (radvd) entries.")


# ===========================================================================
# Entries
# ===========================================================================


@radvd_app.command("list")
@handle_api_errors
def entry_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List radvd entries."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.search_entries(SearchRequest(searchPhrase=search)), lctx.output_format))


@radvd_app.command("get")
@handle_api_errors
def entry_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get an radvd entry by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.get_entry(uuid), lctx.output_format))


@radvd_app.command("del")
@handle_api_errors
def entry_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete an radvd entry."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.del_entry(uuid), lctx.output_format))


@radvd_app.command("toggle")
@handle_api_errors
def entry_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle an radvd entry on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.toggle_entry(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@radvd_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show radvd service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.status(), lctx.output_format))


@radvd_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply radvd configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.reconfigure(), lctx.output_format))


@radvd_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the radvd service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.start(), lctx.output_format))


@radvd_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the radvd service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.stop(), lctx.output_format))


@radvd_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the radvd service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.radvd.restart(), lctx.output_format))
