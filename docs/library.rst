Library Usage
=============

Quick start
-----------

.. code-block:: python

   from opnsense_py import OPNsenseClient

   with OPNsenseClient(
       host="192.168.1.1",
       api_key="your-key",
       api_secret="your-secret",
       verify_ssl=False,       # common for self-signed certs
   ) as client:
       # List firewall aliases
       aliases = client.firewall.search_aliases()
       for alias in aliases.rows:
           print(alias.name, alias.type)

Always use the client as a context manager so the underlying HTTP connection
pool is closed on exit.  Alternatively, call ``client.close()`` explicitly.

Constructor options
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Description
   * - ``host``
     - *(required)*
     - Hostname or IP address of the OPNsense firewall.
   * - ``api_key``
     - *(required)*
     - API key from *System → Access → Users → API keys*.
   * - ``api_secret``
     - *(required)*
     - Corresponding API secret.
   * - ``verify_ssl``
     - ``True``
     - Set to ``False`` to skip TLS certificate verification (self-signed certs).
   * - ``timeout``
     - ``30.0``
     - HTTP request timeout in seconds.
   * - ``port``
     - ``None``
     - Override the default port (443 for HTTPS, 80 for HTTP).
   * - ``https``
     - ``True``
     - Set to ``False`` to use plain HTTP.

Working with modules
--------------------

All API modules are accessed as attributes on the client and are lazily
instantiated on first access:

.. code-block:: python

   client.cron          # CronModule
   client.firewall      # FirewallModule
   client.unbound       # UnboundModule
   client.firmware      # FirmwareModule
   # … see Modules Overview for the full list

See :doc:`modules_overview` for a complete list of available modules.

CRUD operations
---------------

Every module follows the same pattern:

.. code-block:: python

   from opnsense_py.models.cron import CronJob

   # Search (paginated)
   page = client.cron.search_jobs()
   print(page.total, "jobs found")
   for job in page.rows:
       print(job.uuid, job.description)

   # Create
   result = client.cron.add_job(CronJob(
       command="firmware",
       description="Nightly firmware check",
       minutes="0", hours="2",
       days="*", months="*", weekdays="*",
   ))
   new_uuid = result.uuid

   # Read
   job = client.cron.get_job(new_uuid)

   # Update
   job.description = "Updated description"
   client.cron.set_job(new_uuid, job)

   # Toggle enabled state
   client.cron.toggle_job(new_uuid, enabled=False)

   # Delete
   client.cron.del_job(new_uuid)

   # Apply changes to crontab
   client.cron.reconfigure()

Pagination
----------

``search_*`` methods return a :class:`~opnsense_py.models.base.SearchResponse`
envelope with ``rows``, ``total``, ``current``, and ``rowCount`` fields.
Pass a :class:`~opnsense_py.models.base.SearchRequest` to control page size
and filtering:

.. code-block:: python

   from opnsense_py.models.base import SearchRequest

   page = client.cron.search_jobs(SearchRequest(
       current=1,
       rowCount=20,
       searchPhrase="firmware",
   ))

To fetch *all* rows automatically (handles pagination internally), use the
``_search_all`` helper available on every module:

.. code-block:: python

   all_jobs = client.cron._search_all("cron", "settings", "search_jobs")
   print(f"Total: {len(all_jobs)}")

Error handling
--------------

All exceptions inherit from :exc:`~opnsense_py.exceptions.OPNsenseError`:

.. code-block:: python

   from opnsense_py.exceptions import (
       OPNsenseAuthError,
       OPNsenseNotFoundError,
       OPNsenseValidationError,
       OPNsenseHTTPError,
       OPNsenseError,
   )

   try:
       job = client.cron.get_job("nonexistent-uuid")
   except OPNsenseNotFoundError:
       print("Job not found")
   except OPNsenseAuthError:
       print("Invalid API credentials")
   except OPNsenseValidationError as exc:
       print("Validation errors:", exc.validations)
   except OPNsenseHTTPError as exc:
       print(f"HTTP {exc.status_code}: {exc}")
   except OPNsenseError as exc:
       print(f"API error: {exc}")

Exception hierarchy:

.. code-block:: text

   OPNsenseError
   ├── OPNsenseHTTPError        (HTTP 4xx/5xx)
   │   ├── OPNsenseAuthError    (HTTP 401 / 403)
   │   └── OPNsenseNotFoundError (HTTP 404)
   └── OPNsenseValidationError  (HTTP 200 with validation errors in body)

Firewall savepoints
-------------------

The :class:`~opnsense_py.modules.core.firewall.FirewallModule` provides a
``savepoint()`` context manager for safely testing rule changes.  The server
auto-reverts after 60 seconds unless ``cancel_rollback()`` is called:

.. code-block:: python

   with client.firewall.savepoint("filter") as revision:
       client.firewall.toggle_filter_rule(rule_uuid, enabled=False)
       client.firewall.apply(revision)
       # Verify the change worked, then make it permanent:
       client.firewall.cancel_rollback(revision)

Architecture
------------

The client is structured in layers:

1. **OPNsenseClient** — top-level entry point; manages an ``httpx.Client`` with
   Basic Auth. All API modules are lazy-loaded as ``@cached_property`` attributes.

2. **BaseModule** — base class providing generic CRUD helpers (``_search``,
   ``_search_all``, ``_get_item``, ``_add_item``, ``_set_item``, ``_del_item``,
   ``_toggle_item``) and service control helpers (``_service_start``,
   ``_service_stop``, ``_service_restart``, ``_service_reconfigure``,
   ``_service_status``).

3. **Module classes** (``modules/core/``, ``modules/plugins/``) — one per
   OPNsense subsystem, returning typed Pydantic models.

4. **Pydantic models** (``models/``) — typed representations of OPNsense
   entities; all extend :class:`~opnsense_py.models.base.OPNsenseModel` with
   ``extra="allow"`` so unrecognised fields are preserved.

5. **Exceptions** — see `Error handling`_ above.
