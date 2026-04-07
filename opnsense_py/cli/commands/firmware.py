from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render

firmware_app = typer.Typer(name="firmware", help="Manage firmware, updates, and packages.")


# ===========================================================================
# Status / info
# ===========================================================================


@firmware_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show current firmware status and available updates."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.status(), lctx.output_format))


@firmware_app.command("info")
@handle_api_errors
def info(ctx: typer.Context) -> None:
    """Show detailed firmware information."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.info(), lctx.output_format))


@firmware_app.command("running")
@handle_api_errors
def running(ctx: typer.Context) -> None:
    """Check if a firmware operation is in progress."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.running(), lctx.output_format))


@firmware_app.command("connection")
@handle_api_errors
def connection(ctx: typer.Context) -> None:
    """Test connectivity to the firmware mirror."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.connection(), lctx.output_format))


# ===========================================================================
# Operations (fire-and-observe)
# ===========================================================================


@firmware_app.command("check")
@handle_api_errors
def check(ctx: typer.Context) -> None:
    """Check for available firmware updates."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.check(), lctx.output_format))


@firmware_app.command("update")
@handle_api_errors
def update(ctx: typer.Context) -> None:
    """Trigger a firmware update. Poll 'running' to track completion."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.update(), lctx.output_format))


@firmware_app.command("upgrade")
@handle_api_errors
def upgrade(ctx: typer.Context) -> None:
    """Trigger a major firmware upgrade. Poll 'running' to track completion."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.upgrade(), lctx.output_format))


@firmware_app.command("health")
@handle_api_errors
def health(ctx: typer.Context) -> None:
    """Run a firmware health check."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.health(), lctx.output_format))


@firmware_app.command("audit")
@handle_api_errors
def audit(ctx: typer.Context) -> None:
    """Run a firmware security audit."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.audit(), lctx.output_format))


@firmware_app.command("changelog")
@handle_api_errors
def changelog(
    ctx: typer.Context,
    version: Annotated[str, typer.Argument()],
) -> None:
    """Show the changelog for a specific firmware version."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.changelog(version), lctx.output_format))


# ===========================================================================
# System power (requires explicit confirmation)
# ===========================================================================


@firmware_app.command("reboot")
@handle_api_errors
def reboot(
    ctx: typer.Context,
    yes: Annotated[bool, typer.Option("--yes", help="Confirm reboot.")] = False,
) -> None:
    """Reboot the system. Requires --yes."""
    if not yes:
        typer.echo("Missing option '--yes'.", err=True)
        raise typer.Exit(2)
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.reboot(), lctx.output_format))


@firmware_app.command("poweroff")
@handle_api_errors
def poweroff(
    ctx: typer.Context,
    yes: Annotated[bool, typer.Option("--yes", help="Confirm power off.")] = False,
) -> None:
    """Power off the system. Requires --yes."""
    if not yes:
        typer.echo("Missing option '--yes'.", err=True)
        raise typer.Exit(2)
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.poweroff(), lctx.output_format))


# ===========================================================================
# Package management
# ===========================================================================

package_app = typer.Typer(name="package", help="Manage OPNsense packages and plugins.")
firmware_app.add_typer(package_app)


@package_app.command("details")
@handle_api_errors
def package_details(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
) -> None:
    """Show details for a package."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.package_details(name), lctx.output_format))


@package_app.command("install")
@handle_api_errors
def package_install(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
) -> None:
    """Install a package. Poll 'firmware running' to track progress."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.install_package(name), lctx.output_format))


@package_app.command("remove")
@handle_api_errors
def package_remove(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
) -> None:
    """Remove a package."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.remove_package(name), lctx.output_format))


@package_app.command("reinstall")
@handle_api_errors
def package_reinstall(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
) -> None:
    """Reinstall a package."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.reinstall_package(name), lctx.output_format))


@package_app.command("lock")
@handle_api_errors
def package_lock(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
) -> None:
    """Lock a package at its current version."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.lock_package(name), lctx.output_format))


@package_app.command("unlock")
@handle_api_errors
def package_unlock(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
) -> None:
    """Unlock a package so it can be upgraded."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firmware.unlock_package(name), lctx.output_format))
