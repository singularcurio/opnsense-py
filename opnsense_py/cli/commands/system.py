from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.models.base import SearchRequest

system_app = typer.Typer(name="system", help="System control: services, tunables, backups, reboot.")


# ===========================================================================
# System status / control
# ===========================================================================


@system_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show system status messages."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.system_status(), lctx.output_format))


@system_app.command("reboot")
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
    typer.echo(render(lctx.client.core.reboot(), lctx.output_format))


@system_app.command("halt")
@handle_api_errors
def halt(
    ctx: typer.Context,
    yes: Annotated[bool, typer.Option("--yes", help="Confirm halt.")] = False,
) -> None:
    """Halt the system. Requires --yes."""
    if not yes:
        typer.echo("Missing option '--yes'.", err=True)
        raise typer.Exit(2)
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.halt(), lctx.output_format))


# ===========================================================================
# Services
# ===========================================================================

service_app = typer.Typer(name="service", help="Manage system services.")
system_app.add_typer(service_app)


@service_app.command("list")
@handle_api_errors
def service_list(ctx: typer.Context) -> None:
    """List all services and their status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.search_services(), lctx.output_format))


@service_app.command("start")
@handle_api_errors
def service_start(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
    service_id: Annotated[str, typer.Option("--id", help="Optional service instance ID.")] = "",
) -> None:
    """Start a service by name."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.start_service(name, service_id), lctx.output_format))


@service_app.command("stop")
@handle_api_errors
def service_stop(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
    service_id: Annotated[str, typer.Option("--id")] = "",
) -> None:
    """Stop a service by name."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.stop_service(name, service_id), lctx.output_format))


@service_app.command("restart")
@handle_api_errors
def service_restart(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument()],
    service_id: Annotated[str, typer.Option("--id")] = "",
) -> None:
    """Restart a service by name."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.restart_service(name, service_id), lctx.output_format))


# ===========================================================================
# Tunables
# ===========================================================================

tunable_app = typer.Typer(name="tunable", help="Manage sysctl tunables.")
system_app.add_typer(tunable_app)


@tunable_app.command("list")
@handle_api_errors
def tunable_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List tunables."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.search_tunables(SearchRequest(searchPhrase=search)), lctx.output_format))


@tunable_app.command("get")
@handle_api_errors
def tunable_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a tunable by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.get_tunable(uuid), lctx.output_format))


@tunable_app.command("del")
@handle_api_errors
def tunable_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a tunable override."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.del_tunable(uuid), lctx.output_format))


@tunable_app.command("reconfigure")
@handle_api_errors
def tunable_reconfigure(ctx: typer.Context) -> None:
    """Apply tunable changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.reconfigure_tunables(), lctx.output_format))


# ===========================================================================
# Backups
# ===========================================================================

backup_app = typer.Typer(name="backup", help="Manage configuration backups.")
system_app.add_typer(backup_app)


@backup_app.command("list")
@handle_api_errors
def backup_list(
    ctx: typer.Context,
    host: Annotated[str, typer.Argument()],
) -> None:
    """List backups for a host."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.list_backups(host), lctx.output_format))


@backup_app.command("revert")
@handle_api_errors
def backup_revert(
    ctx: typer.Context,
    backup: Annotated[str, typer.Argument()],
) -> None:
    """Revert to a backup."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.revert_backup(backup), lctx.output_format))


@backup_app.command("delete")
@handle_api_errors
def backup_delete(
    ctx: typer.Context,
    backup: Annotated[str, typer.Argument()],
) -> None:
    """Delete a backup."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.core.delete_backup(backup), lctx.output_format))
