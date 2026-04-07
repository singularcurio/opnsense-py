from __future__ import annotations

from enum import Enum
from functools import wraps
from typing import Annotated, Any, Callable, TypeVar

import typer

from opnsense_py.cli.context import build_client
from opnsense_py.exceptions import (
    OPNsenseAuthError,
    OPNsenseError,
    OPNsenseHTTPError,
    OPNsenseNotFoundError,
    OPNsenseValidationError,
)

F = TypeVar("F", bound=Callable[..., Any])


class OutputFormat(str, Enum):
    table = "table"
    json = "json"
    plain = "plain"


# ---------------------------------------------------------------------------
# Error handler decorator
# ---------------------------------------------------------------------------


def handle_api_errors(f: F) -> F:
    """Decorator that catches OPNsense exceptions and exits with a clean message."""

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except OPNsenseValidationError as exc:
            typer.echo("Validation errors:", err=True)
            for field, msg in exc.validations.items():
                typer.echo(f"  {field}: {msg}", err=True)
            raise typer.Exit(code=4)
        except OPNsenseAuthError:
            typer.echo("Authentication failed. Check your API key and secret.", err=True)
            raise typer.Exit(code=2)
        except OPNsenseNotFoundError as exc:
            typer.echo(f"Not found: {exc}", err=True)
            raise typer.Exit(code=3)
        except OPNsenseHTTPError as exc:
            typer.echo(f"HTTP error: {exc}", err=True)
            raise typer.Exit(code=1)
        except OPNsenseError as exc:
            typer.echo(f"API error: {exc}", err=True)
            raise typer.Exit(code=1)

    return wrapper  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Root app
# ---------------------------------------------------------------------------

app = typer.Typer(help="opn — OPNsense command-line interface.")


@app.callback()
def cli(
    ctx: typer.Context,
    host: Annotated[str | None, typer.Option(envvar="OPNSENSE_HOST", help="OPNsense hostname or IP.")] = None,
    api_key: Annotated[str | None, typer.Option(envvar="OPNSENSE_API_KEY", help="API key.")] = None,
    api_secret: Annotated[str | None, typer.Option(envvar="OPNSENSE_API_SECRET", help="API secret.")] = None,
    no_verify_ssl: Annotated[bool, typer.Option("--no-verify-ssl/--verify-ssl", help="Disable TLS certificate verification.")] = False,
    no_tls: Annotated[bool, typer.Option("--no-tls/--tls", envvar="OPNSENSE_NO_TLS", help="Use plain HTTP instead of HTTPS.")] = False,
    profile: Annotated[str, typer.Option(envvar="OPNSENSE_PROFILE", help="Config file profile to use.")] = "default",
    output: Annotated[OutputFormat, typer.Option("-o", "--output", help="Output format.")] = OutputFormat.table,
) -> None:
    # Allow tests to inject a pre-built _LazyContext via obj=
    if isinstance(ctx.obj, _LazyContext):
        return
    ctx.obj = _LazyContext(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        verify_ssl=not no_verify_ssl,
        https=not no_tls,
        profile=profile,
        output_format=output.value,
    )
    ctx.call_on_close(_close_client(ctx))


def _close_client(ctx: typer.Context) -> Callable[[], None]:
    def _close() -> None:
        lazy = ctx.obj
        if isinstance(lazy, _LazyContext) and lazy._client is not None:
            lazy._client.close()

    return _close


class _LazyContext:
    """Defers client construction until the first command actually needs it."""

    def __init__(
        self,
        host: str | None,
        api_key: str | None,
        api_secret: str | None,
        verify_ssl: bool,
        https: bool,
        profile: str,
        output_format: str,
    ) -> None:
        self._host = host
        self._api_key = api_key
        self._api_secret = api_secret
        self._verify_ssl = verify_ssl
        self._https = https
        self._profile = profile
        self.output_format = output_format
        self._client = None

    @property
    def client(self):  # type: ignore[no-untyped-def]
        if self._client is None:
            self._client = build_client(
                host=self._host,
                api_key=self._api_key,
                api_secret=self._api_secret,
                verify_ssl=self._verify_ssl,
                https=self._https,
                profile=self._profile,
            )
        return self._client


def get_ctx(ctx: typer.Context) -> _LazyContext:
    """Retrieve the _LazyContext from the Typer context object."""
    return ctx.obj  # type: ignore[no-any-return]


# ---------------------------------------------------------------------------
# Subgroup registration
# ---------------------------------------------------------------------------

from opnsense_py.cli.commands.auth import auth_app  # noqa: E402
from opnsense_py.cli.commands.captiveportal import captiveportal_app  # noqa: E402
from opnsense_py.cli.commands.cron import cron_app  # noqa: E402
from opnsense_py.cli.commands.dhcrelay import dhcrelay_app  # noqa: E402
from opnsense_py.cli.commands.diagnostics import diagnostics_app  # noqa: E402
from opnsense_py.cli.commands.dnsmasq import dnsmasq_app  # noqa: E402
from opnsense_py.cli.commands.firewall import firewall_app  # noqa: E402
from opnsense_py.cli.commands.firmware import firmware_app  # noqa: E402
from opnsense_py.cli.commands.haproxy import haproxy_app  # noqa: E402
from opnsense_py.cli.commands.hostdiscovery import hostdiscovery_app  # noqa: E402
from opnsense_py.cli.commands.ids import ids_app  # noqa: E402
from opnsense_py.cli.commands.ipsec import ipsec_app  # noqa: E402
from opnsense_py.cli.commands.kea import kea_app  # noqa: E402
from opnsense_py.cli.commands.monit import monit_app  # noqa: E402
from opnsense_py.cli.commands.ntpd import ntpd_app  # noqa: E402
from opnsense_py.cli.commands.openvpn import openvpn_app  # noqa: E402
from opnsense_py.cli.commands.radvd import radvd_app  # noqa: E402
from opnsense_py.cli.commands.routes import routes_app  # noqa: E402
from opnsense_py.cli.commands.routing import routing_app  # noqa: E402
from opnsense_py.cli.commands.syslog import syslog_app  # noqa: E402
from opnsense_py.cli.commands.system import system_app  # noqa: E402
from opnsense_py.cli.commands.trafficshaper import trafficshaper_app  # noqa: E402
from opnsense_py.cli.commands.trust import trust_app  # noqa: E402
from opnsense_py.cli.commands.unbound import unbound_app  # noqa: E402
from opnsense_py.cli.commands.wireguard import wireguard_app  # noqa: E402

app.add_typer(auth_app)
app.add_typer(captiveportal_app)
app.add_typer(cron_app)
app.add_typer(dhcrelay_app)
app.add_typer(diagnostics_app)
app.add_typer(dnsmasq_app)
app.add_typer(firewall_app)
app.add_typer(firmware_app)
app.add_typer(haproxy_app)
app.add_typer(hostdiscovery_app)
app.add_typer(ids_app)
app.add_typer(ipsec_app)
app.add_typer(kea_app)
app.add_typer(monit_app)
app.add_typer(ntpd_app)
app.add_typer(openvpn_app)
app.add_typer(radvd_app)
app.add_typer(routes_app)
app.add_typer(routing_app)
app.add_typer(syslog_app)
app.add_typer(system_app)
app.add_typer(trafficshaper_app)
app.add_typer(trust_app)
app.add_typer(unbound_app)
app.add_typer(wireguard_app)
