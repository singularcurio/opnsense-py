from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.models.base import SearchRequest

trust_app = typer.Typer(name="trust", help="Manage certificate authorities, certificates, and CRLs.")


# ===========================================================================
# Certificate Authorities
# ===========================================================================

ca_app = typer.Typer(name="ca", help="Manage certificate authorities.")
trust_app.add_typer(ca_app)


@ca_app.command("list")
@handle_api_errors
def ca_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List certificate authorities."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.search_cas(SearchRequest(searchPhrase=search)), lctx.output_format))


@ca_app.command("get")
@handle_api_errors
def ca_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a CA by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.get_ca(uuid), lctx.output_format))


@ca_app.command("del")
@handle_api_errors
def ca_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a CA."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.del_ca(uuid), lctx.output_format))


@ca_app.command("dump")
@handle_api_errors
def ca_dump(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Dump the raw PEM of a CA."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.raw_dump_ca(uuid), lctx.output_format))


# ===========================================================================
# Certificates
# ===========================================================================

cert_app = typer.Typer(name="cert", help="Manage certificates.")
trust_app.add_typer(cert_app)


@cert_app.command("list")
@handle_api_errors
def cert_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List certificates."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.search_certs(SearchRequest(searchPhrase=search)), lctx.output_format))


@cert_app.command("get")
@handle_api_errors
def cert_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a certificate by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.get_cert(uuid), lctx.output_format))


@cert_app.command("del")
@handle_api_errors
def cert_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a certificate."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.del_cert(uuid), lctx.output_format))


@cert_app.command("dump")
@handle_api_errors
def cert_dump(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Dump the raw PEM of a certificate."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.raw_dump_cert(uuid), lctx.output_format))


# ===========================================================================
# CRLs
# ===========================================================================

crl_app = typer.Typer(name="crl", help="Manage certificate revocation lists.")
trust_app.add_typer(crl_app)


@crl_app.command("list")
@handle_api_errors
def crl_list(ctx: typer.Context) -> None:
    """List CRLs."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.search_crls(), lctx.output_format))


@crl_app.command("get")
@handle_api_errors
def crl_get(
    ctx: typer.Context,
    caref: Annotated[str, typer.Argument()],
) -> None:
    """Get CRL for a CA (by CA ref)."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.get_crl(caref), lctx.output_format))


@crl_app.command("del")
@handle_api_errors
def crl_del(
    ctx: typer.Context,
    caref: Annotated[str, typer.Argument()],
) -> None:
    """Delete the CRL for a CA."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.del_crl(caref), lctx.output_format))


@crl_app.command("dump")
@handle_api_errors
def crl_dump(
    ctx: typer.Context,
    caref: Annotated[str, typer.Argument()],
) -> None:
    """Dump the raw PEM of a CRL."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.raw_dump_crl(caref), lctx.output_format))


# ===========================================================================
# Reconfigure
# ===========================================================================


@trust_app.command("reconfigure")
@handle_api_errors
def reconfigure(ctx: typer.Context) -> None:
    """Apply trust store configuration."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.trust.reconfigure(), lctx.output_format))
