from __future__ import annotations

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render

hostdiscovery_app = typer.Typer(name="hostdiscovery", help="Discover hosts on the network via ARP/NDP scanning.")


@hostdiscovery_app.command("scan")
@handle_api_errors
def scan(ctx: typer.Context) -> None:
    """Show discovered hosts."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.hostdiscovery.search(), lctx.output_format))


@hostdiscovery_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show host discovery service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.hostdiscovery.status(), lctx.output_format))


@hostdiscovery_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply host discovery configuration."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.hostdiscovery.reconfigure(), lctx.output_format))


@hostdiscovery_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the host discovery service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.hostdiscovery.start(), lctx.output_format))


@hostdiscovery_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the host discovery service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.hostdiscovery.stop(), lctx.output_format))


@hostdiscovery_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the host discovery service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.hostdiscovery.restart(), lctx.output_format))
