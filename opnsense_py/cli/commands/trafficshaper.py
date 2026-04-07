from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.trafficshaper import ShaperPipe, ShaperQueue, ShaperRule

trafficshaper_app = typer.Typer(name="trafficshaper", help="Manage traffic shaper pipes, queues, and rules.")


# ===========================================================================
# Pipes
# ===========================================================================

pipe_app = typer.Typer(name="pipe", help="Manage traffic shaper pipes.")
trafficshaper_app.add_typer(pipe_app)


@pipe_app.command("list")
@handle_api_errors
def pipe_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List shaper pipes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.search_pipes(SearchRequest(searchPhrase=search)), lctx.output_format))


@pipe_app.command("get")
@handle_api_errors
def pipe_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a pipe by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.get_pipe(uuid), lctx.output_format))


@pipe_app.command("add")
@handle_api_errors
def pipe_add(
    ctx: typer.Context,
    bandwidth: Annotated[int | None, typer.Option(help="Bandwidth in Kbit/s.")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a shaper pipe."""
    lctx = get_ctx(ctx)
    obj = build_model(ShaperPipe, from_json, bandwidth=bandwidth,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.trafficshaper.add_pipe(obj), lctx.output_format))


@pipe_app.command("set")
@handle_api_errors
def pipe_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    bandwidth: Annotated[int | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a shaper pipe."""
    lctx = get_ctx(ctx)
    obj = build_model(ShaperPipe, from_json, bandwidth=bandwidth,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.trafficshaper.set_pipe(uuid, obj), lctx.output_format))


@pipe_app.command("del")
@handle_api_errors
def pipe_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a shaper pipe."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.del_pipe(uuid), lctx.output_format))


@pipe_app.command("toggle")
@handle_api_errors
def pipe_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a shaper pipe."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.toggle_pipe(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Queues
# ===========================================================================

queue_app = typer.Typer(name="queue", help="Manage traffic shaper queues.")
trafficshaper_app.add_typer(queue_app)


@queue_app.command("list")
@handle_api_errors
def queue_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List shaper queues."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.search_queues(SearchRequest(searchPhrase=search)), lctx.output_format))


@queue_app.command("get")
@handle_api_errors
def queue_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a queue by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.get_queue(uuid), lctx.output_format))


@queue_app.command("add")
@handle_api_errors
def queue_add(
    ctx: typer.Context,
    pipe: Annotated[str | None, typer.Option(help="Parent pipe UUID.")] = None,
    weight: Annotated[int | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a shaper queue."""
    lctx = get_ctx(ctx)
    obj = build_model(ShaperQueue, from_json, pipe=pipe, weight=weight,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.trafficshaper.add_queue(obj), lctx.output_format))


@queue_app.command("set")
@handle_api_errors
def queue_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    pipe: Annotated[str | None, typer.Option()] = None,
    weight: Annotated[int | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a shaper queue."""
    lctx = get_ctx(ctx)
    obj = build_model(ShaperQueue, from_json, pipe=pipe, weight=weight,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.trafficshaper.set_queue(uuid, obj), lctx.output_format))


@queue_app.command("del")
@handle_api_errors
def queue_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a shaper queue."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.del_queue(uuid), lctx.output_format))


@queue_app.command("toggle")
@handle_api_errors
def queue_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a shaper queue."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.toggle_queue(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Rules
# ===========================================================================

rule_app = typer.Typer(name="rule", help="Manage traffic shaper rules.")
trafficshaper_app.add_typer(rule_app)


@rule_app.command("list")
@handle_api_errors
def rule_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List shaper rules."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.search_rules(SearchRequest(searchPhrase=search)), lctx.output_format))


@rule_app.command("get")
@handle_api_errors
def rule_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a shaper rule by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.get_rule(uuid), lctx.output_format))


@rule_app.command("add")
@handle_api_errors
def rule_add(
    ctx: typer.Context,
    interface: Annotated[str | None, typer.Option()] = None,
    proto: Annotated[str | None, typer.Option(help="Protocol (tcp, udp, etc.)")] = None,
    source: Annotated[str | None, typer.Option()] = None,
    destination: Annotated[str | None, typer.Option()] = None,
    target: Annotated[str | None, typer.Option(help="Target pipe or queue UUID.")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a shaper rule."""
    lctx = get_ctx(ctx)
    obj = build_model(ShaperRule, from_json, interface=interface, proto=proto,
                      source=source, destination=destination, target=target,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.trafficshaper.add_rule(obj), lctx.output_format))


@rule_app.command("set")
@handle_api_errors
def rule_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    interface: Annotated[str | None, typer.Option()] = None,
    proto: Annotated[str | None, typer.Option()] = None,
    source: Annotated[str | None, typer.Option()] = None,
    destination: Annotated[str | None, typer.Option()] = None,
    target: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a shaper rule."""
    lctx = get_ctx(ctx)
    obj = build_model(ShaperRule, from_json, interface=interface, proto=proto,
                      source=source, destination=destination, target=target,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.trafficshaper.set_rule(uuid, obj), lctx.output_format))


@rule_app.command("del")
@handle_api_errors
def rule_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a shaper rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.del_rule(uuid), lctx.output_format))


@rule_app.command("toggle")
@handle_api_errors
def rule_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a shaper rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.toggle_rule(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@trafficshaper_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply traffic shaper configuration."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.reconfigure(), lctx.output_format))


@trafficshaper_app.command("statistics")
@handle_api_errors
def statistics(ctx: typer.Context) -> None:
    """Show traffic shaper statistics."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trafficshaper.statistics(), lctx.output_format))
