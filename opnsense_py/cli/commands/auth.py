from __future__ import annotations

from typing import Annotated

import typer

from opnsense_py.cli.main import get_ctx, handle_api_errors
from opnsense_py.cli.output import render
from opnsense_py.models.base import SearchRequest

auth_app = typer.Typer(name="auth", help="Manage users, groups, and API keys.")


# ===========================================================================
# Users
# ===========================================================================

user_app = typer.Typer(name="user", help="Manage local user accounts.")
auth_app.add_typer(user_app)


@user_app.command("list")
@handle_api_errors
def user_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List users."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.search_users(SearchRequest(searchPhrase=search)), lctx.output_format))


@user_app.command("get")
@handle_api_errors
def user_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a user by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.get_user(uuid), lctx.output_format))


@user_app.command("del")
@handle_api_errors
def user_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a user."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.del_user(uuid), lctx.output_format))


@user_app.command("api-keys")
@handle_api_errors
def api_keys(ctx: typer.Context) -> None:
    """List all API keys."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.search_api_keys(), lctx.output_format))


@user_app.command("add-api-key")
@handle_api_errors
def add_api_key(
    ctx: typer.Context,
    username: Annotated[str, typer.Argument()],
) -> None:
    """Generate a new API key for a user."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.add_api_key(username), lctx.output_format))


@user_app.command("del-api-key")
@handle_api_errors
def del_api_key(
    ctx: typer.Context,
    key_id: Annotated[str, typer.Argument()],
) -> None:
    """Delete an API key by ID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.del_api_key(key_id), lctx.output_format))


# ===========================================================================
# Groups
# ===========================================================================

group_app = typer.Typer(name="group", help="Manage local user groups.")
auth_app.add_typer(group_app)


@group_app.command("list")
@handle_api_errors
def group_list(
    ctx: typer.Context,
    search: Annotated[str, typer.Option(help="Filter by search phrase.")] = "",
) -> None:
    """List groups."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.search_groups(SearchRequest(searchPhrase=search)), lctx.output_format))


@group_app.command("get")
@handle_api_errors
def group_get(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Get a group by UUID."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.get_group(uuid), lctx.output_format))


@group_app.command("del")
@handle_api_errors
def group_del(
    ctx: typer.Context,
    uuid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a group."""
    lctx = get_ctx(ctx)
    typer.echo(render(lctx.client.auth.del_group(uuid), lctx.output_format))
