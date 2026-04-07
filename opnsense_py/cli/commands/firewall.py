from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.cli.utils import build_model
from opnsense_py.models.base import SearchRequest
from opnsense_py.models.firewall import DNatRule, FilterRule, FirewallAlias, SNatRule

firewall_app = typer.Typer(name="firewall", help="Manage firewall rules, aliases, and NAT.")


# ===========================================================================
# Aliases
# ===========================================================================

alias_app = typer.Typer(name="alias", help="Manage firewall aliases.")
firewall_app.add_typer(alias_app)


@alias_app.command("list")
@handle_api_errors
def alias_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List firewall aliases."""
    lctx = get_ctx(ctx)
    result = lctx.client.firewall.search_aliases(SearchRequest(searchPhrase=search))
    typer.echo(render(result, lctx.output_format))


@alias_app.command("get")
@handle_api_errors
def alias_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a firewall alias by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.get_alias(uuid), lctx.output_format))


@alias_app.command("add")
@handle_api_errors
def alias_add(
    ctx: typer.Context,
    name: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type", metavar="TYPE", help="host, network, port, url, ...")] = None,
    content: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option(help='"1" or "0".')] = None,
    proto: Annotated[str | None, typer.Option()] = None,
    interface: Annotated[str | None, typer.Option()] = None,
    updatefreq: Annotated[str | None, typer.Option()] = None,
    categories: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a firewall alias."""
    lctx = get_ctx(ctx)
    obj = build_model(FirewallAlias, from_json, name=name, type=type_, content=content,
                      description=description, enabled=enabled, proto=proto,
                      interface=interface, updatefreq=updatefreq, categories=categories)
    typer.echo(render(lctx.client.firewall.add_alias(obj), lctx.output_format))


@alias_app.command("set")
@handle_api_errors
def alias_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    name: Annotated[str | None, typer.Option()] = None,
    type_: Annotated[str | None, typer.Option("--type", metavar="TYPE")] = None,
    content: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    enabled: Annotated[str | None, typer.Option()] = None,
    proto: Annotated[str | None, typer.Option()] = None,
    interface: Annotated[str | None, typer.Option()] = None,
    updatefreq: Annotated[str | None, typer.Option()] = None,
    categories: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a firewall alias."""
    lctx = get_ctx(ctx)
    obj = build_model(FirewallAlias, from_json, name=name, type=type_, content=content,
                      description=description, enabled=enabled, proto=proto,
                      interface=interface, updatefreq=updatefreq, categories=categories)
    typer.echo(render(lctx.client.firewall.set_alias(uuid, obj), lctx.output_format))


@alias_app.command("del")
@handle_api_errors
def alias_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a firewall alias."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.del_alias(uuid), lctx.output_format))


@alias_app.command("toggle")
@handle_api_errors
def alias_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a firewall alias on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.toggle_alias(uuid, enabled=enable), lctx.output_format))


@alias_app.command("reconfigure")
@handle_api_errors
def alias_reconfigure(ctx: typer.Context) -> None:
    """Apply alias configuration changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.reconfigure_aliases(), lctx.output_format))


# ===========================================================================
# Filter rules
# ===========================================================================

rule_app = typer.Typer(name="rule", help="Manage firewall filter rules.")
firewall_app.add_typer(rule_app)


@rule_app.command("list")
@handle_api_errors
def rule_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List firewall filter rules."""
    lctx = get_ctx(ctx)
    result = lctx.client.firewall.search_filter_rules(SearchRequest(searchPhrase=search))
    typer.echo(render(result, lctx.output_format))


@rule_app.command("get")
@handle_api_errors
def rule_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a firewall rule by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.get_filter_rule(uuid), lctx.output_format))


@rule_app.command("add")
@handle_api_errors
def rule_add(
    ctx: typer.Context,
    enabled: Annotated[str | None, typer.Option()] = None,
    action: Annotated[str | None, typer.Option(help="pass, block, reject")] = None,
    interface: Annotated[str | None, typer.Option()] = None,
    direction: Annotated[str | None, typer.Option(help="in, out")] = None,
    protocol: Annotated[str | None, typer.Option()] = None,
    source_net: Annotated[str | None, typer.Option("--source-net")] = None,
    source_port: Annotated[str | None, typer.Option("--source-port")] = None,
    destination_net: Annotated[str | None, typer.Option("--destination-net")] = None,
    destination_port: Annotated[str | None, typer.Option("--destination-port")] = None,
    gateway: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    log: Annotated[str | None, typer.Option()] = None,
    sequence: Annotated[str | None, typer.Option()] = None,
    ipprotocol: Annotated[str | None, typer.Option(help="inet, inet6")] = None,
    quick: Annotated[str | None, typer.Option()] = None,
    categories: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a firewall filter rule."""
    lctx = get_ctx(ctx)
    obj = build_model(FilterRule, from_json, enabled=enabled, action=action,
                      interface=interface, direction=direction, protocol=protocol,
                      source_net=source_net, source_port=source_port,
                      destination_net=destination_net, destination_port=destination_port,
                      gateway=gateway, description=description, log=log,
                      sequence=sequence, ipprotocol=ipprotocol, quick=quick,
                      categories=categories)
    typer.echo(render(lctx.client.firewall.add_filter_rule(obj), lctx.output_format))


@rule_app.command("set")
@handle_api_errors
def rule_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enabled: Annotated[str | None, typer.Option()] = None,
    action: Annotated[str | None, typer.Option(help="pass, block, reject")] = None,
    interface: Annotated[str | None, typer.Option()] = None,
    direction: Annotated[str | None, typer.Option(help="in, out")] = None,
    protocol: Annotated[str | None, typer.Option()] = None,
    source_net: Annotated[str | None, typer.Option("--source-net")] = None,
    source_port: Annotated[str | None, typer.Option("--source-port")] = None,
    destination_net: Annotated[str | None, typer.Option("--destination-net")] = None,
    destination_port: Annotated[str | None, typer.Option("--destination-port")] = None,
    gateway: Annotated[str | None, typer.Option()] = None,
    description: Annotated[str | None, typer.Option()] = None,
    log: Annotated[str | None, typer.Option()] = None,
    sequence: Annotated[str | None, typer.Option()] = None,
    ipprotocol: Annotated[str | None, typer.Option(help="inet, inet6")] = None,
    quick: Annotated[str | None, typer.Option()] = None,
    categories: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a firewall filter rule."""
    lctx = get_ctx(ctx)
    obj = build_model(FilterRule, from_json, enabled=enabled, action=action,
                      interface=interface, direction=direction, protocol=protocol,
                      source_net=source_net, source_port=source_port,
                      destination_net=destination_net, destination_port=destination_port,
                      gateway=gateway, description=description, log=log,
                      sequence=sequence, ipprotocol=ipprotocol, quick=quick,
                      categories=categories)
    typer.echo(render(lctx.client.firewall.set_filter_rule(uuid, obj), lctx.output_format))


@rule_app.command("del")
@handle_api_errors
def rule_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a firewall filter rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.del_filter_rule(uuid), lctx.output_format))


@rule_app.command("toggle")
@handle_api_errors
def rule_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a firewall filter rule on or off."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.toggle_filter_rule(uuid, enabled=enable), lctx.output_format))


# ===========================================================================
# Destination NAT (port forwards)
# ===========================================================================

dnat_app = typer.Typer(name="dnat", help="Manage destination NAT (port forward) rules.")
firewall_app.add_typer(dnat_app)


@dnat_app.command("list")
@handle_api_errors
def dnat_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List DNAT rules."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.search_dnat_rules(SearchRequest(searchPhrase=search)), lctx.output_format))


@dnat_app.command("get")
@handle_api_errors
def dnat_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a DNAT rule by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.get_dnat_rule(uuid), lctx.output_format))


@dnat_app.command("add")
@handle_api_errors
def dnat_add(
    ctx: typer.Context,
    interface: Annotated[str | None, typer.Option()] = None,
    protocol: Annotated[str | None, typer.Option()] = None,
    target: Annotated[str | None, typer.Option()] = None,
    local_port: Annotated[str | None, typer.Option("--local-port")] = None,
    descr: Annotated[str | None, typer.Option("--description")] = None,
    log: Annotated[str | None, typer.Option()] = None,
    sequence: Annotated[str | None, typer.Option()] = None,
    disabled: Annotated[str | None, typer.Option()] = None,
    ipprotocol: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a DNAT rule."""
    lctx = get_ctx(ctx)
    obj = build_model(DNatRule, from_json, interface=interface, protocol=protocol,
                      target=target, local_port=local_port, descr=descr, log=log,
                      sequence=sequence, disabled=disabled, ipprotocol=ipprotocol)
    typer.echo(render(lctx.client.firewall.add_dnat_rule(obj), lctx.output_format))


@dnat_app.command("set")
@handle_api_errors
def dnat_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    interface: Annotated[str | None, typer.Option()] = None,
    protocol: Annotated[str | None, typer.Option()] = None,
    target: Annotated[str | None, typer.Option()] = None,
    local_port: Annotated[str | None, typer.Option("--local-port")] = None,
    descr: Annotated[str | None, typer.Option("--description")] = None,
    log: Annotated[str | None, typer.Option()] = None,
    sequence: Annotated[str | None, typer.Option()] = None,
    disabled: Annotated[str | None, typer.Option()] = None,
    ipprotocol: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a DNAT rule."""
    lctx = get_ctx(ctx)
    obj = build_model(DNatRule, from_json, interface=interface, protocol=protocol,
                      target=target, local_port=local_port, descr=descr, log=log,
                      sequence=sequence, disabled=disabled, ipprotocol=ipprotocol)
    typer.echo(render(lctx.client.firewall.set_dnat_rule(uuid, obj), lctx.output_format))


@dnat_app.command("del")
@handle_api_errors
def dnat_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a DNAT rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.del_dnat_rule(uuid), lctx.output_format))


@dnat_app.command("toggle")
@handle_api_errors
def dnat_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a DNAT rule. Note: the API uses a 'disabled' flag, so --disable enables it."""
    lctx = get_ctx(ctx)
    disabled = (not enable) if enable is not None else None
    typer.echo(render(lctx.client.firewall.toggle_dnat_rule(uuid, disabled=disabled), lctx.output_format))


# ===========================================================================
# Source NAT (outbound)
# ===========================================================================

snat_app = typer.Typer(name="snat", help="Manage source NAT (outbound) rules.")
firewall_app.add_typer(snat_app)


@snat_app.command("list")
@handle_api_errors
def snat_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List SNAT rules."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.search_snat_rules(SearchRequest(searchPhrase=search)), lctx.output_format))


@snat_app.command("get")
@handle_api_errors
def snat_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a SNAT rule by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.get_snat_rule(uuid), lctx.output_format))


@snat_app.command("add")
@handle_api_errors
def snat_add(
    ctx: typer.Context,
    interface: Annotated[str | None, typer.Option()] = None,
    protocol: Annotated[str | None, typer.Option()] = None,
    source_net: Annotated[str | None, typer.Option("--source-net")] = None,
    source_port: Annotated[str | None, typer.Option("--source-port")] = None,
    destination_net: Annotated[str | None, typer.Option("--destination-net")] = None,
    destination_port: Annotated[str | None, typer.Option("--destination-port")] = None,
    target: Annotated[str | None, typer.Option()] = None,
    target_port: Annotated[str | None, typer.Option("--target-port")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    log: Annotated[str | None, typer.Option()] = None,
    sequence: Annotated[str | None, typer.Option()] = None,
    disabled: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Add a SNAT rule."""
    lctx = get_ctx(ctx)
    obj = build_model(SNatRule, from_json, interface=interface, protocol=protocol,
                      source_net=source_net, source_port=source_port,
                      destination_net=destination_net, destination_port=destination_port,
                      target=target, target_port=target_port, description=description,
                      log=log, sequence=sequence, enabled="0" if disabled == "1" else None)
    typer.echo(render(lctx.client.firewall.add_snat_rule(obj), lctx.output_format))


@snat_app.command("set")
@handle_api_errors
def snat_set(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    interface: Annotated[str | None, typer.Option()] = None,
    protocol: Annotated[str | None, typer.Option()] = None,
    source_net: Annotated[str | None, typer.Option("--source-net")] = None,
    source_port: Annotated[str | None, typer.Option("--source-port")] = None,
    destination_net: Annotated[str | None, typer.Option("--destination-net")] = None,
    destination_port: Annotated[str | None, typer.Option("--destination-port")] = None,
    target: Annotated[str | None, typer.Option()] = None,
    target_port: Annotated[str | None, typer.Option("--target-port")] = None,
    description: Annotated[str | None, typer.Option()] = None,
    log: Annotated[str | None, typer.Option()] = None,
    sequence: Annotated[str | None, typer.Option()] = None,
    from_json: Annotated[str | None, typer.Option("--from-json", metavar="FILE|-")] = None,
) -> None:
    """Update a SNAT rule."""
    lctx = get_ctx(ctx)
    obj = build_model(SNatRule, from_json, interface=interface, protocol=protocol,
                      source_net=source_net, source_port=source_port,
                      destination_net=destination_net, destination_port=destination_port,
                      target=target, target_port=target_port, description=description,
                      log=log, sequence=sequence)
    typer.echo(render(lctx.client.firewall.set_snat_rule(uuid, obj), lctx.output_format))


@snat_app.command("del")
@handle_api_errors
def snat_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a SNAT rule."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.del_snat_rule(uuid), lctx.output_format))


@snat_app.command("toggle")
@handle_api_errors
def snat_toggle(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
    enable: Annotated[bool | None, typer.Option("--enable/--disable")] = None,
) -> None:
    """Toggle a SNAT rule on or off."""
    lctx = get_ctx(ctx)
    disabled = (not enable) if enable is not None else None
    typer.echo(render(lctx.client.firewall.toggle_snat_rule(uuid, disabled=disabled), lctx.output_format))


# ===========================================================================
# Top-level apply
# ===========================================================================


@firewall_app.command("apply")
@handle_api_errors
def apply(ctx: typer.Context) -> None:
    """Apply pending firewall changes."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.firewall.apply(), lctx.output_format))
