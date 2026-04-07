from __future__ import annotations

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render

ntpd_app = typer.Typer(name="ntpd", help="Show NTP daemon status and peer information.")


@ntpd_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show NTP service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ntpd.status(), lctx.output_format))


@ntpd_app.command("peers")
@handle_api_errors
def peers(ctx: typer.Context) -> None:
    """Show NTP peer metadata."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ntpd.meta(), lctx.output_format))


@ntpd_app.command("gps")
@handle_api_errors
def gps(ctx: typer.Context) -> None:
    """Show GPS source status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.ntpd.gps(), lctx.output_format))
