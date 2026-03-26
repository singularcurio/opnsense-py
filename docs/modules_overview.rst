Modules Overview
================

All modules are accessed as attributes on :class:`~opnsense_py.OPNsenseClient`
and are instantiated lazily on first access.

.. code-block:: python

   with OPNsenseClient(host=..., api_key=..., api_secret=...) as client:
       client.cron        # CronModule
       client.firewall    # FirewallModule
       client.unbound     # UnboundModule
       # etc.

Core modules
------------

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Attribute
     - Class
     - Description
   * - ``client.auth``
     - ``AuthModule``
     - Users, groups, and API key management
   * - ``client.captiveportal``
     - ``CaptivePortalModule``
     - Captive portal zones, sessions, and vouchers
   * - ``client.core``
     - ``CoreModule``
     - System-level core API (firmware, tunables)
   * - ``client.cron``
     - ``CronModule``
     - Cron job scheduling
   * - ``client.dhcrelay``
     - ``DhcrelayModule``
     - DHCP relay configuration
   * - ``client.diagnostics``
     - ``DiagnosticsModule``
     - ARP table, routing table, firewall states, traffic stats
   * - ``client.dnsmasq``
     - ``DnsmasqModule``
     - Dnsmasq DNS/DHCP host entries and domain overrides
   * - ``client.firewall``
     - ``FirewallModule``
     - Aliases, filter rules, DNAT, SNAT, NPT, one-to-one NAT
   * - ``client.firmware``
     - ``FirmwareModule``
     - Firmware updates and package management
   * - ``client.hostdiscovery``
     - ``HostdiscoveryModule``
     - Network host scanning
   * - ``client.ids``
     - ``IdsModule``
     - Suricata IDS/IPS policies, rules, and alerts
   * - ``client.interfaces``
     - ``InterfacesModule``
     - Network interface configuration
   * - ``client.ipsec``
     - ``IpsecModule``
     - IPsec VPN connections, child SAs, and sessions
   * - ``client.kea``
     - ``KeaModule``
     - Kea DHCP server subnets and reservations
   * - ``client.monit``
     - ``MonitModule``
     - Monit service checks, tests, and alert configurations
   * - ``client.ntpd``
     - ``NtpdModule``
     - NTP daemon status
   * - ``client.openvpn``
     - ``OpenVpnModule``
     - OpenVPN instances, client overwrites, and sessions
   * - ``client.radvd``
     - ``RadvdModule``
     - Router Advertisement daemon configuration
   * - ``client.routes``
     - ``RoutesModule``
     - Static routes
   * - ``client.routing``
     - ``RoutingModule``
     - Gateway definitions
   * - ``client.syslog``
     - ``SyslogModule``
     - Remote syslog destination configuration
   * - ``client.trafficshaper``
     - ``TrafficShaperModule``
     - Traffic shaper pipes, queues, and rules
   * - ``client.trust``
     - ``TrustModule``
     - Certificate authorities, certificates, and CRLs
   * - ``client.unbound``
     - ``UnboundModule``
     - Unbound DNS resolver hosts, forwards, and ACLs
   * - ``client.wireguard``
     - ``WireguardModule``
     - WireGuard VPN servers and peers

Plugin modules
--------------

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Attribute
     - Class
     - Description
   * - ``client.haproxy``
     - ``HaproxyModule``
     - HAProxy frontends, backends, and servers

Common method patterns
----------------------

Every module exposes a consistent set of methods based on the resource type.
Below is the pattern using ``cron`` as an example — the same shape applies to
all modules.

**Search / list**

.. code-block:: python

   page = client.cron.search_jobs()        # SearchResponse[CronJob]
   page.total    # total row count
   page.rows     # list of CronJob objects

**Get one item**

.. code-block:: python

   job = client.cron.get_job(uuid)         # CronJob

**Create**

.. code-block:: python

   result = client.cron.add_job(CronJob(...))   # ApiResponse
   result.uuid   # UUID of the new job

**Update**

.. code-block:: python

   result = client.cron.set_job(uuid, job)      # ApiResponse

**Delete**

.. code-block:: python

   result = client.cron.del_job(uuid)           # ApiResponse

**Toggle enabled**

.. code-block:: python

   client.cron.toggle_job(uuid)             # flip current state
   client.cron.toggle_job(uuid, enabled=True)   # force enable

**Apply / reconfigure**

.. code-block:: python

   client.cron.reconfigure()               # writes changes to disk/daemon

Service control
---------------

Modules that wrap a running service expose additional helpers inherited from
:class:`~opnsense_py.modules.base.BaseModule`:

.. code-block:: python

   client.unbound._service_start("unbound")
   client.unbound._service_stop("unbound")
   client.unbound._service_restart("unbound")
   client.unbound._service_reconfigure("unbound")
   status = client.unbound._service_status("unbound")
