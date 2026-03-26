CLI Reference
=============

The ``opn`` (and ``opnsense``) command provides a full CLI over the OPNsense REST API.

Quick start
-----------

.. code-block:: bash

   # HTTPS with self-signed certificate (most common)
   opn --host 192.168.1.1 --no-verify-ssl --api-key KEY --api-secret SECRET system status

   # Plain HTTP
   opn --host 192.168.1.1 --no-tls --api-key KEY --api-secret SECRET system status

   # With a config file profile (see Configuration file below)
   opn system status

Configuration file
------------------

Store connection settings in ``~/.config/opnsense-py/config.toml`` to avoid
repeating flags on every invocation:

.. code-block:: toml

   [default]
   host = "192.168.1.1"
   api_key = "your-key"
   api_secret = "your-secret"
   verify_ssl = "false"

   [prod]
   host = "firewall.example.com"
   api_key = "prod-key"
   api_secret = "prod-secret"

Switch profiles with ``--profile prod`` or ``OPNSENSE_PROFILE=prod``.

Settings are resolved in this order (highest priority first):

1. CLI flags (``--host``, ``--api-key``, …)
2. Environment variables (``OPNSENSE_HOST``, …)
3. Config file profile

Environment variables
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Description
   * - ``OPNSENSE_HOST``
     - Hostname or IP
   * - ``OPNSENSE_API_KEY``
     - API key
   * - ``OPNSENSE_API_SECRET``
     - API secret
   * - ``OPNSENSE_VERIFY_SSL``
     - Set to ``false`` to skip TLS verification
   * - ``OPNSENSE_NO_TLS``
     - Set to ``1`` to use plain HTTP
   * - ``OPNSENSE_PROFILE``
     - Config file profile (default: ``default``)

Global flags
------------

These flags are accepted before the command group:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Flag
     - Description
   * - ``--host TEXT``
     - OPNsense hostname or IP
   * - ``--api-key TEXT``
     - API key
   * - ``--api-secret TEXT``
     - API secret
   * - ``--no-verify-ssl``
     - Disable TLS certificate verification
   * - ``--no-tls``
     - Use plain HTTP instead of HTTPS
   * - ``--profile TEXT``
     - Config file profile to use
   * - ``-o, --output [table|json|plain]``
     - Output format (default: ``table``)

Output formats
--------------

.. code-block:: bash

   opn -o table firewall alias list   # default: human-readable table
   opn -o json  firewall alias list   # JSON array (pipe-friendly)
   opn -o plain firewall alias list   # one UUID/value per line

The ``plain`` format is useful for scripting:

.. code-block:: bash

   # Delete all cron jobs matching a search
   opn -o plain cron list-jobs | xargs -I{} opn cron del-job {}

Available command groups
------------------------

Run any command with ``--help`` for full usage, e.g. ``opn cron --help``.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Group
     - Description
   * - ``auth``
     - Users, groups, API keys
   * - ``captiveportal``
     - Captive portal zones, sessions, vouchers
   * - ``cron``
     - Cron jobs (list, add, set, del, toggle, reconfigure)
   * - ``dhcrelay``
     - DHCP relay configuration
   * - ``diagnostics``
     - ARP table, routes, interfaces, firewall states, traffic
   * - ``dnsmasq``
     - Dnsmasq DNS/DHCP host entries and domain overrides
   * - ``firewall``
     - Aliases, filter rules, NAT rules (DNAT / SNAT / NPT / one-to-one)
   * - ``firmware``
     - Firmware updates and package management
   * - ``haproxy``
     - HAProxy frontends, backends, servers
   * - ``hostdiscovery``
     - Network host scanning
   * - ``ids``
     - Suricata IDS/IPS policies, rules, alerts
   * - ``ipsec``
     - IPsec VPN connections, child SAs, sessions
   * - ``kea``
     - Kea DHCP subnets and reservations
   * - ``monit``
     - Monit service checks, tests, alerts
   * - ``ntpd``
     - NTP daemon status
   * - ``openvpn``
     - OpenVPN instances, overwrites, sessions
   * - ``radvd``
     - Router Advertisement daemon configuration
   * - ``routes``
     - Static routes
   * - ``routing``
     - Gateway definitions
   * - ``syslog``
     - Remote syslog destinations
   * - ``system``
     - System status, services, tunables, backups, reboot
   * - ``trafficshaper``
     - Traffic shaper pipes, queues, rules
   * - ``trust``
     - Certificate authorities, certificates, CRLs
   * - ``unbound``
     - Unbound DNS resolver hosts, forwards, ACLs
   * - ``wireguard``
     - WireGuard VPN servers and peers

Cron example (full CRUD workflow)
----------------------------------

.. code-block:: bash

   # List all jobs
   opn cron list-jobs

   # Add a job (individual flags)
   opn cron add-job \
     --command firmware \
     --description "Nightly firmware check" \
     --minutes 0 --hours 2 \
     --days '*' --months '*' --weekdays '*'

   # Add a job from JSON
   opn cron add-job --from-json - <<EOF
   {"command":"firmware","description":"Nightly check","minutes":"0","hours":"2","days":"*","months":"*","weekdays":"*"}
   EOF

   # Get a specific job
   opn cron get-job <uuid>

   # Update a job
   opn cron set-job <uuid> --description "Updated description"

   # Toggle enabled state
   opn cron toggle-job <uuid>
   opn cron toggle-job <uuid> --enable
   opn cron toggle-job <uuid> --disable

   # Delete a job
   opn cron del-job <uuid>

   # Apply pending changes
   opn cron reconfigure

Firewall alias example
----------------------

.. code-block:: bash

   # List aliases
   opn firewall alias list

   # Add an alias
   opn firewall alias add \
     --name MY_SERVERS \
     --type host \
     --content "10.0.0.1\n10.0.0.2" \
     --description "My servers"

   # Delete an alias
   opn firewall alias del <uuid>

   # Reconfigure (apply changes)
   opn firewall alias reconfigure

Exit codes
----------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Exit code
     - Meaning
   * - ``0``
     - Success
   * - ``1``
     - General / unexpected error
   * - ``2``
     - Authentication error (invalid API credentials)
   * - ``3``
     - Resource not found (404)
   * - ``4``
     - Validation error (API returned validation failures)
