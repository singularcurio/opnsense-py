from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any

import httpx

from opnsense_py.exceptions import (
    OPNsenseAuthError,
    OPNsenseError,
    OPNsenseHTTPError,
    OPNsenseNotFoundError,
    OPNsenseValidationError,
)

if TYPE_CHECKING:
    from opnsense_py.modules.core.auth import AuthModule
    from opnsense_py.modules.core.captiveportal import CaptivePortalModule
    from opnsense_py.modules.core.core import CoreModule
    from opnsense_py.modules.core.cron import CronModule
    from opnsense_py.modules.core.dhcrelay import DhcrelayModule
    from opnsense_py.modules.core.diagnostics import DiagnosticsModule
    from opnsense_py.modules.core.dnsmasq import DnsmasqModule
    from opnsense_py.modules.core.firewall import FirewallModule
    from opnsense_py.modules.core.firmware import FirmwareModule
    from opnsense_py.modules.core.hostdiscovery import HostdiscoveryModule
    from opnsense_py.modules.core.ids import IdsModule
    from opnsense_py.modules.core.interfaces import InterfacesModule
    from opnsense_py.modules.core.ipsec import IpsecModule
    from opnsense_py.modules.core.kea import KeaModule
    from opnsense_py.modules.core.monit import MonitModule
    from opnsense_py.modules.core.ntpd import NtpdModule
    from opnsense_py.modules.core.openvpn import OpenVpnModule
    from opnsense_py.modules.core.radvd import RadvdModule
    from opnsense_py.modules.core.routes import RoutesModule
    from opnsense_py.modules.core.routing import RoutingModule
    from opnsense_py.modules.core.syslog import SyslogModule
    from opnsense_py.modules.core.trafficshaper import TrafficShaperModule
    from opnsense_py.modules.core.trust import TrustModule
    from opnsense_py.modules.core.unbound import UnboundModule
    from opnsense_py.modules.core.wireguard import WireguardModule
    from opnsense_py.modules.plugins.haproxy import HaproxyModule


class OPNsenseClient:
    """
    HTTP client for the OPNsense REST API.

    Usage::

        with OPNsenseClient(host="192.168.1.1", api_key="...", api_secret="...") as client:
            jobs = client.cron.search_jobs()
    """

    def __init__(
        self,
        host: str,
        api_key: str,
        api_secret: str,
        verify_ssl: bool = True,
        timeout: float = 30.0,
        port: int | None = None,
        https: bool = True,
    ) -> None:
        """
        Create a new OPNsense API client.

        :param host: Hostname or IP address of the OPNsense firewall.
        :param api_key: API key from *System → Access → Users → API keys*.
        :param api_secret: Corresponding API secret.
        :param verify_ssl: Verify the server's TLS certificate.
            Set to ``False`` for self-signed certificates.
        :param timeout: HTTP request timeout in seconds (default 30).
        :param port: Override the default port (443 for HTTPS, 80 for HTTP).
        :param https: Use HTTPS (default). Set to ``False`` for plain HTTP.
        """
        scheme = "https" if https else "http"
        resolved_port = port if port is not None else (443 if https else 80)
        self._base_url = f"{scheme}://{host}:{resolved_port}/api/"
        self._http = httpx.Client(
            base_url=self._base_url,
            auth=(api_key, api_secret),
            verify=verify_ssl if https else False,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> OPNsenseClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    # ------------------------------------------------------------------
    # Low-level HTTP methods
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._http.get(path, params=params)
        return self._handle_response(response)

    def _post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        response = self._http.post(path, json=json or {}, params=params)
        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        if response.status_code in (301, 302, 307, 308):
            location = response.headers.get("location", "")
            hint = ""
            if location.startswith("https://"):
                hint = " The server is redirecting to HTTPS — try removing --no-tls and adding --no-verify-ssl instead."
            raise OPNsenseError(
                f"Unexpected redirect (HTTP {response.status_code}) to: {location or '<no location>'}.{hint}"
            )
        if response.status_code in (401, 403):
            raise OPNsenseAuthError(response.status_code, response.text)
        if response.status_code == 404:
            raise OPNsenseNotFoundError(response.status_code, response.text)
        if response.status_code >= 400:
            raise OPNsenseHTTPError(response.status_code, response.text)

        try:
            data: dict[str, Any] = response.json()
        except Exception as exc:
            content_type = response.headers.get("content-type", "unknown")
            raise OPNsenseError(
                f"Non-JSON response (HTTP {response.status_code}, "
                f"Content-Type: {content_type}, URL: {response.url}): "
                f"{response.text[:500] or '<empty body>'}"
            ) from exc

        if data.get("validations"):
            raise OPNsenseValidationError(data["validations"])

        return data

    # ------------------------------------------------------------------
    # Module accessors (lazy-loaded)
    # ------------------------------------------------------------------

    @cached_property
    def auth(self) -> AuthModule:
        from opnsense_py.modules.core.auth import AuthModule
        return AuthModule(self)

    @cached_property
    def captiveportal(self) -> CaptivePortalModule:
        from opnsense_py.modules.core.captiveportal import CaptivePortalModule
        return CaptivePortalModule(self)

    @cached_property
    def core(self) -> CoreModule:
        from opnsense_py.modules.core.core import CoreModule
        return CoreModule(self)

    @cached_property
    def cron(self) -> CronModule:
        from opnsense_py.modules.core.cron import CronModule
        return CronModule(self)

    @cached_property
    def dhcrelay(self) -> DhcrelayModule:
        from opnsense_py.modules.core.dhcrelay import DhcrelayModule
        return DhcrelayModule(self)

    @cached_property
    def diagnostics(self) -> DiagnosticsModule:
        from opnsense_py.modules.core.diagnostics import DiagnosticsModule
        return DiagnosticsModule(self)

    @cached_property
    def dnsmasq(self) -> DnsmasqModule:
        from opnsense_py.modules.core.dnsmasq import DnsmasqModule
        return DnsmasqModule(self)

    @cached_property
    def firewall(self) -> FirewallModule:
        from opnsense_py.modules.core.firewall import FirewallModule
        return FirewallModule(self)

    @cached_property
    def firmware(self) -> FirmwareModule:
        from opnsense_py.modules.core.firmware import FirmwareModule
        return FirmwareModule(self)

    @cached_property
    def hostdiscovery(self) -> HostdiscoveryModule:
        from opnsense_py.modules.core.hostdiscovery import HostdiscoveryModule
        return HostdiscoveryModule(self)

    @cached_property
    def ids(self) -> IdsModule:
        from opnsense_py.modules.core.ids import IdsModule
        return IdsModule(self)

    @cached_property
    def interfaces(self) -> InterfacesModule:
        from opnsense_py.modules.core.interfaces import InterfacesModule
        return InterfacesModule(self)

    @cached_property
    def ipsec(self) -> IpsecModule:
        from opnsense_py.modules.core.ipsec import IpsecModule
        return IpsecModule(self)

    @cached_property
    def kea(self) -> KeaModule:
        from opnsense_py.modules.core.kea import KeaModule
        return KeaModule(self)

    @cached_property
    def monit(self) -> MonitModule:
        from opnsense_py.modules.core.monit import MonitModule
        return MonitModule(self)

    @cached_property
    def ntpd(self) -> NtpdModule:
        from opnsense_py.modules.core.ntpd import NtpdModule
        return NtpdModule(self)

    @cached_property
    def openvpn(self) -> OpenVpnModule:
        from opnsense_py.modules.core.openvpn import OpenVpnModule
        return OpenVpnModule(self)

    @cached_property
    def radvd(self) -> RadvdModule:
        from opnsense_py.modules.core.radvd import RadvdModule
        return RadvdModule(self)

    @cached_property
    def routes(self) -> RoutesModule:
        from opnsense_py.modules.core.routes import RoutesModule
        return RoutesModule(self)

    @cached_property
    def routing(self) -> RoutingModule:
        from opnsense_py.modules.core.routing import RoutingModule
        return RoutingModule(self)

    @cached_property
    def syslog(self) -> SyslogModule:
        from opnsense_py.modules.core.syslog import SyslogModule
        return SyslogModule(self)

    @cached_property
    def trafficshaper(self) -> TrafficShaperModule:
        from opnsense_py.modules.core.trafficshaper import TrafficShaperModule
        return TrafficShaperModule(self)

    @cached_property
    def trust(self) -> TrustModule:
        from opnsense_py.modules.core.trust import TrustModule
        return TrustModule(self)

    @cached_property
    def unbound(self) -> UnboundModule:
        from opnsense_py.modules.core.unbound import UnboundModule
        return UnboundModule(self)

    @cached_property
    def wireguard(self) -> WireguardModule:
        from opnsense_py.modules.core.wireguard import WireguardModule
        return WireguardModule(self)

    @cached_property
    def haproxy(self) -> HaproxyModule:
        from opnsense_py.modules.plugins.haproxy import HaproxyModule
        return HaproxyModule(self)
