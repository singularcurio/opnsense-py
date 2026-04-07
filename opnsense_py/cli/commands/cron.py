from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.cron import CronJob

cron_app = typer.Typer(name="cron", help="Manage cron jobs.")


# ---------------------------------------------------------------------------
# list-jobs
# ---------------------------------------------------------------------------


@cron_app.command("list-jobs")
@handle_api_errors
def list_jobs(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List all cron jobs."""
    lctx = get_ctx(ctx)
    from opnsense_py.models.base import SearchRequest

    result = lctx.client.cron.search_jobs(SearchRequest(searchPhrase=search))
    typer.echo(render(result, lctx.output_format))


# ---------------------------------------------------------------------------
# get-job
# ---------------------------------------------------------------------------


@cron_app.command("get-job")
@handle_api_errors
def get_job(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a cron job by UUID."""
    lctx = get_ctx(ctx)
    result = lctx.client.cron.get_job(uuid)
    typer.echo(render(result, lctx.output_format))


# ---------------------------------------------------------------------------
# add-job
# ---------------------------------------------------------------------------


@cron_app.command("add-job")
@handle_api_errors
def add_job(
    ctx: typer.Context,
    minutes: Annotated[str | None, typer.Option()] = None,
    hours: Annotated[str | None, typer.Option()] = None,
    days: Annotated[str | None, typer.Option()] = None,
    months: Annotated[str | None, typer.Option()] = None,
    weekdays: Annotated[str | None, typer.Option()] = None,
    who: Annotated[str | None, typer.Option()] = None,
    command: Annotated[str | None, typer.Option()] = None,
    parameters: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option(help='"1" to enable, "0" to disable.')] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-", help="Read job fields from JSON (use - for stdin).")] = None,
) -> None:
    """Add a new cron job."""
    lctx = get_ctx(ctx)
    job = build_model(
        CronJob,
        from_json,
        minutes=minutes,
        hours=hours,
        days=days,
        months=months,
        weekdays=weekdays,
        who=who,
        command=command,
        parameters=parameters,
        description=description,
        enabled=enabled,
    )
    result = lctx.client.cron.add_job(job)
    typer.echo(render(result, lctx.output_format))


# ---------------------------------------------------------------------------
# set-job
# ---------------------------------------------------------------------------


@cron_app.command("set-job")
@handle_api_errors
def set_job(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    minutes: Annotated[str | None, typer.Option()] = None,
    hours: Annotated[str | None, typer.Option()] = None,
    days: Annotated[str | None, typer.Option()] = None,
    months: Annotated[str | None, typer.Option()] = None,
    weekdays: Annotated[str | None, typer.Option()] = None,
    who: Annotated[str | None, typer.Option()] = None,
    command: Annotated[str | None, typer.Option()] = None,
    parameters: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option(help='"1" to enable, "0" to disable.')] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-", help="Read job fields from JSON (use - for stdin).")] = None,
) -> None:
    """Update an existing cron job."""
    lctx = get_ctx(ctx)
    job = build_model(
        CronJob,
        from_json,
        minutes=minutes,
        hours=hours,
        days=days,
        months=months,
        weekdays=weekdays,
        who=who,
        command=command,
        parameters=parameters,
        description=description,
        enabled=enabled,
    )
    result = lctx.client.cron.set_job(uuid, job)
    typer.echo(render(result, lctx.output_format))


# ---------------------------------------------------------------------------
# del-job
# ---------------------------------------------------------------------------


@cron_app.command("del-job")
@handle_api_errors
def del_job(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a cron job."""
    lctx = get_ctx(ctx)
    result = lctx.client.cron.del_job(uuid)
    typer.echo(render(result, lctx.output_format))


# ---------------------------------------------------------------------------
# toggle-job
# ---------------------------------------------------------------------------


@cron_app.command("toggle-job")
@handle_api_errors
def toggle_job(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable", help="Set enabled state explicitly.")] = None,
) -> None:
    """Toggle a cron job on or off."""
    lctx = get_ctx(ctx)
    result = lctx.client.cron.toggle_job(uuid, enabled=enable)
    typer.echo(render(result, lctx.output_format))


# ---------------------------------------------------------------------------
# reconfigure
# ---------------------------------------------------------------------------


@cron_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply cron configuration changes."""
    lctx = get_ctx(ctx)
    result = lctx.client.cron.reconfigure()
    typer.echo(render(result, lctx.output_format))
