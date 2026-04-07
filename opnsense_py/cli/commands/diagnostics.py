from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render

diagnostics_app = typer.Typer(name="diagnostics", help="System diagnostics: ARP, routes, states, interfaces, traffic.")


# ===========================================================================
# System info
# ===========================================================================


@diagnostics_app.command("info")
@handle_api_errors
def system_info(ctx: typer.Context) -> None:
    """Show system information (uptime, version, CPU, etc.)."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.system_information(), lctx.output_format))


@diagnostics_app.command("resources")
@handle_api_errors
def resources(ctx: typer.Context) -> None:
    """Show CPU, memory, and disk resource usage."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.system_resources(), lctx.output_format))


@diagnostics_app.command("memory")
@handle_api_errors
def memory(ctx: typer.Context) -> None:
    """Show detailed memory statistics."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.system_memory(), lctx.output_format))


@diagnostics_app.command("disk")
@handle_api_errors
def disk(ctx: typer.Context) -> None:
    """Show disk usage."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.system_disk(), lctx.output_format))


@diagnostics_app.command("temperature")
@handle_api_errors
def temperature(ctx: typer.Context) -> None:
    """Show hardware temperature sensors."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.system_temperature(), lctx.output_format))


@diagnostics_app.command("time")
@handle_api_errors
def time(ctx: typer.Context) -> None:
    """Show system time."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.system_time(), lctx.output_format))


# ===========================================================================
# ARP / NDP
# ===========================================================================


@diagnostics_app.command("arp")
@handle_api_errors
def arp(ctx: typer.Context) -> None:
    """Show ARP table."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.search_arp(), lctx.output_format))


@diagnostics_app.command("ndp")
@handle_api_errors
def ndp(ctx: typer.Context) -> None:
    """Show IPv6 NDP neighbor table."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.search_ndp(), lctx.output_format))


@diagnostics_app.command("flush-arp")
@handle_api_errors
def flush_arp(ctx: typer.Context) -> None:
    """Flush the ARP table."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.flush_arp(), lctx.output_format))


# ===========================================================================
# Routes
# ===========================================================================


@diagnostics_app.command("routes")
@handle_api_errors
def routes(ctx: typer.Context) -> None:
    """Show the kernel routing table."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_routes(), lctx.output_format))


# ===========================================================================
# Interfaces
# ===========================================================================


@diagnostics_app.command("interfaces")
@handle_api_errors
def interfaces(ctx: typer.Context) -> None:
    """Show interface statistics."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_interface_statistics(), lctx.output_format))


@diagnostics_app.command("interface-names")
@handle_api_errors
def interface_names(ctx: typer.Context) -> None:
    """List interface names."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_interface_names(), lctx.output_format))


@diagnostics_app.command("vip-status")
@handle_api_errors
def vip_status(ctx: typer.Context) -> None:
    """Show CARP/VIP status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_vip_status(), lctx.output_format))


# ===========================================================================
# Firewall states
# ===========================================================================


@diagnostics_app.command("states")
@handle_api_errors
def states(ctx: typer.Context) -> None:
    """Show firewall state table summary."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_pf_states(), lctx.output_format))


@diagnostics_app.command("flush-states")
@handle_api_errors
def flush_states(ctx: typer.Context) -> None:
    """Flush all firewall states."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.flush_states(), lctx.output_format))


@diagnostics_app.command("pf-stats")
@handle_api_errors
def pf_stats(
    ctx: typer.Context,
    section: Annotated[str | None, typer.Option(help="Specific statistics section.")] = None,
) -> None:
    """Show pf statistics."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_pf_statistics(section), lctx.output_format))


# ===========================================================================
# Traffic
# ===========================================================================


@diagnostics_app.command("traffic")
@handle_api_errors
def traffic(ctx: typer.Context) -> None:
    """Show live interface traffic counters."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.traffic_interface(), lctx.output_format))


@diagnostics_app.command("activity")
@handle_api_errors
def activity(ctx: typer.Context) -> None:
    """Show system process activity (top)."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.diagnostics.get_activity(), lctx.output_format))
