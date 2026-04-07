from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.dnsmasq import DnsmasqDomainOverride, DnsmasqHost

dnsmasq_app = typer.Typer(name="dnsmasq", help="Manage Dnsmasq DNS/DHCP host entries and domain overrides.")


# ===========================================================================
# Hosts
# ===========================================================================

host_app = typer.Typer(name="host", help="Manage Dnsmasq host entries.")
dnsmasq_app.add_typer(host_app)


@host_app.command("list")
@handle_api_errors
def host_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List host entries."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.search_hosts(SearchRequest(searchPhrase=search)), lctx.output_format))


@host_app.command("get")
@handle_api_errors
def host_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a host entry by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.get_host(uuid), lctx.output_format))


@host_app.command("add")
@handle_api_errors
def host_add(
    ctx: typer.Context,
    hostname: Annotated[str | None, typer.Option()] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    ip: Annotated[str | None, typer.Option(help="IP address.")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a host entry."""
    lctx = get_ctx(ctx)
    obj = build_model(DnsmasqHost, from_json, hostname=hostname, domain=domain,
                      ip=ip, description=description, enabled=enabled)
    typer.echo(render(lctx.client.dnsmasq.add_host(obj), lctx.output_format))


@host_app.command("set")
@handle_api_errors
def host_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    hostname: Annotated[str | None, typer.Option()] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    ip: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a host entry."""
    lctx = get_ctx(ctx)
    obj = build_model(DnsmasqHost, from_json, hostname=hostname, domain=domain,
                      ip=ip, description=description, enabled=enabled)
    typer.echo(render(lctx.client.dnsmasq.set_host(uuid, obj), lctx.output_format))


@host_app.command("del")
@handle_api_errors
def host_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a host entry."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.del_host(uuid), lctx.output_format))


# ===========================================================================
# Domain overrides
# ===========================================================================

domain_app = typer.Typer(name="domain", help="Manage Dnsmasq domain overrides.")
dnsmasq_app.add_typer(domain_app)


@domain_app.command("list")
@handle_api_errors
def domain_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List domain overrides."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.search_domains(SearchRequest(searchPhrase=search)), lctx.output_format))


@domain_app.command("get")
@handle_api_errors
def domain_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a domain override by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.get_domain(uuid), lctx.output_format))


@domain_app.command("add")
@handle_api_errors
def domain_add(
    ctx: typer.Context,
    domain: Annotated[str | None, typer.Option()] = None,
    ip: Annotated[str | None, typer.Option(help="Upstream DNS server IP.")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a domain override."""
    lctx = get_ctx(ctx)
    obj = build_model(DnsmasqDomainOverride, from_json, domain=domain, ip=ip,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.dnsmasq.add_domain(obj), lctx.output_format))


@domain_app.command("set")
@handle_api_errors
def domain_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    domain: Annotated[str | None, typer.Option()] = None,
    ip: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a domain override."""
    lctx = get_ctx(ctx)
    obj = build_model(DnsmasqDomainOverride, from_json, domain=domain, ip=ip,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.dnsmasq.set_domain(uuid, obj), lctx.output_format))


@domain_app.command("del")
@handle_api_errors
def domain_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a domain override."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.del_domain(uuid), lctx.output_format))


# ===========================================================================
# Leases
# ===========================================================================


@dnsmasq_app.command("leases")
@handle_api_errors
def leases(ctx: typer.Context) -> None:
    """Show active DHCP leases."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.search_leases(), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@dnsmasq_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show Dnsmasq service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.status(), lctx.output_format))


@dnsmasq_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply Dnsmasq configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.reconfigure(), lctx.output_format))


@dnsmasq_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the Dnsmasq service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.start(), lctx.output_format))


@dnsmasq_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the Dnsmasq service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.stop(), lctx.output_format))


@dnsmasq_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the Dnsmasq service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.dnsmasq.restart(), lctx.output_format))
