from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.unbound import HostAlias, HostOverride, UnboundAcl, UnboundDot

unbound_app = typer.Typer(name="unbound", help="Manage the Unbound DNS resolver.")


# ===========================================================================
# Host overrides
# ===========================================================================

host_app = typer.Typer(name="host", help="Manage DNS host overrides.")
unbound_app.add_typer(host_app)


@host_app.command("list")
@handle_api_errors
def host_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List host overrides."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.search_host_overrides(SearchRequest(searchPhrase=search)), lctx.output_format))


@host_app.command("get")
@handle_api_errors
def host_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a host override by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.get_host_override(uuid), lctx.output_format))


@host_app.command("add")
@handle_api_errors
def host_add(
    ctx: typer.Context,
    hostname: Annotated[str | None, typer.Option()] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    server: Annotated[str | None, typer.Option(help="IP address the hostname resolves to.")] = None,
    rr: Annotated[str | None, typer.Option(help="Record type: A, AAAA, MX, ...")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    addptr: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a DNS host override."""
    lctx = get_ctx(ctx)
    obj = build_model(HostOverride, from_json, hostname=hostname, domain=domain,
                      server=server, rr=rr, description=description, enabled=enabled,
                      addptr=addptr)
    typer.echo(render(lctx.client.unbound.add_host_override(obj), lctx.output_format))


@host_app.command("set")
@handle_api_errors
def host_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    hostname: Annotated[str | None, typer.Option()] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    server: Annotated[str | None, typer.Option()] = None,
    rr: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    addptr: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a DNS host override."""
    lctx = get_ctx(ctx)
    obj = build_model(HostOverride, from_json, hostname=hostname, domain=domain,
                      server=server, rr=rr, description=description, enabled=enabled,
                      addptr=addptr)
    typer.echo(render(lctx.client.unbound.set_host_override(uuid, obj), lctx.output_format))


@host_app.command("del")
@handle_api_errors
def host_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a DNS host override."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.del_host_override(uuid), lctx.output_format))


@host_app.command("toggle")
@handle_api_errors
def host_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a DNS host override."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.toggle_host_override(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Host aliases
# ===========================================================================

alias_app = typer.Typer(name="alias", help="Manage DNS host aliases (CNAMEs).")
unbound_app.add_typer(alias_app)


@alias_app.command("list")
@handle_api_errors
def alias_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List host aliases."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.search_host_aliases(SearchRequest(searchPhrase=search)), lctx.output_format))


@alias_app.command("get")
@handle_api_errors
def alias_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a host alias by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.get_host_alias(uuid), lctx.output_format))


@alias_app.command("add")
@handle_api_errors
def alias_add(
    ctx: typer.Context,
    host_uuid: Annotated[str | None, typer.Option("--host", help="UUID of the host override to alias.")] = None,
    hostname: Annotated[str | None, typer.Option()] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a host alias."""
    lctx = get_ctx(ctx)
    obj = build_model(HostAlias, from_json, host=host_uuid, hostname=hostname,
                      domain=domain, description=description, enabled=enabled)
    typer.echo(render(lctx.client.unbound.add_host_alias(obj), lctx.output_format))


@alias_app.command("set")
@handle_api_errors
def alias_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    host_uuid: Annotated[str | None, typer.Option("--host")] = None,
    hostname: Annotated[str | None, typer.Option()] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a host alias."""
    lctx = get_ctx(ctx)
    obj = build_model(HostAlias, from_json, host=host_uuid, hostname=hostname,
                      domain=domain, description=description, enabled=enabled)
    typer.echo(render(lctx.client.unbound.set_host_alias(uuid, obj), lctx.output_format))


@alias_app.command("del")
@handle_api_errors
def alias_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a host alias."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.del_host_alias(uuid), lctx.output_format))


@alias_app.command("toggle")
@handle_api_errors
def alias_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a host alias."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.toggle_host_alias(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Forwards (DoT / upstream resolvers)
# ===========================================================================

forward_app = typer.Typer(name="forward", help="Manage DNS forwards and DoT upstreams.")
unbound_app.add_typer(forward_app)


@forward_app.command("list")
@handle_api_errors
def forward_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List DNS forwards."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.search_forwards(SearchRequest(searchPhrase=search)), lctx.output_format))


@forward_app.command("get")
@handle_api_errors
def forward_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a DNS forward by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.get_forward(uuid), lctx.output_format))


@forward_app.command("add")
@handle_api_errors
def forward_add(
    ctx: typer.Context,
    server: Annotated[str | None, typer.Option(help="Upstream resolver IP.")] = None,
    port: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type", help="dot, forward")] = None,
    domain: Annotated[str | None, typer.Option(help="Domain to forward (empty = all).")] = None,
    verify: Annotated[str | None, typer.Option(help="TLS verify hostname.")] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a DNS forward / DoT upstream."""
    lctx = get_ctx(ctx)
    obj = build_model(UnboundDot, from_json, server=server, port=port, type=type_,
                      domain=domain, verify=verify, enabled=enabled, description=description)
    typer.echo(render(lctx.client.unbound.add_forward(obj), lctx.output_format))


@forward_app.command("set")
@handle_api_errors
def forward_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    server: Annotated[str | None, typer.Option()] = None,
    port: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type")] = None,
    domain: Annotated[str | None, typer.Option()] = None,
    verify: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a DNS forward."""
    lctx = get_ctx(ctx)
    obj = build_model(UnboundDot, from_json, server=server, port=port, type=type_,
                      domain=domain, verify=verify, enabled=enabled, description=description)
    typer.echo(render(lctx.client.unbound.set_forward(uuid, obj), lctx.output_format))


@forward_app.command("del")
@handle_api_errors
def forward_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a DNS forward."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.del_forward(uuid), lctx.output_format))


@forward_app.command("toggle")
@handle_api_errors
def forward_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a DNS forward."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.toggle_forward(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# ACLs
# ===========================================================================

acl_app = typer.Typer(name="acl", help="Manage Unbound access control lists.")
unbound_app.add_typer(acl_app)


@acl_app.command("list")
@handle_api_errors
def acl_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List ACL entries."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.search_acls(SearchRequest(searchPhrase=search)), lctx.output_format))


@acl_app.command("get")
@handle_api_errors
def acl_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get an ACL entry by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.get_acl(uuid), lctx.output_format))


@acl_app.command("add")
@handle_api_errors
def acl_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    action: Annotated[str | None, typer.Option(help="allow, refuse, deny, allow_snoop")] = None,
    networks: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add an ACL entry."""
    lctx = get_ctx(ctx)
    obj = build_model(UnboundAcl, from_json, name=name, action=action, networks=networks,
                      description=description, enabled=enabled)
    typer.echo(render(lctx.client.unbound.add_acl(obj), lctx.output_format))


@acl_app.command("del")
@handle_api_errors
def acl_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete an ACL entry."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.del_acl(uuid), lctx.output_format))


# ===========================================================================
# Service control
# ===========================================================================


@unbound_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply Unbound configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.reconfigure(), lctx.output_format))


@unbound_app.command("status")
@handle_api_errors
def status(ctx: typer.Context) -> None:
    """Show Unbound service status."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.status(), lctx.output_format))


@unbound_app.command("start")
@handle_api_errors
def start(ctx: typer.Context) -> None:
    """Start the Unbound service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.start(), lctx.output_format))


@unbound_app.command("stop")
@handle_api_errors
def stop(ctx: typer.Context) -> None:
    """Stop the Unbound service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.stop(), lctx.output_format))


@unbound_app.command("restart")
@handle_api_errors
def restart(ctx: typer.Context) -> None:
    """Restart the Unbound service."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.unbound.restart(), lctx.output_format))
