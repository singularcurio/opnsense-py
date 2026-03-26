Contributing
============

Development setup
-----------------

.. code-block:: bash

   git clone https://github.com/yourusername/opnsense-py
   cd opnsense-py
   poetry install --extras cli

Running tests
-------------

Unit tests use ``respx`` to mock ``httpx`` at the transport level — no live
OPNsense instance is required:

.. code-block:: bash

   # Run all unit tests
   poetry run pytest

   # Run a single test file
   poetry run pytest tests/unit/modules/core/test_cron.py

   # Run a single test
   poetry run pytest tests/unit/modules/core/test_cron.py::test_search_jobs

Integration tests require a live OPNsense instance and are skipped by default:

.. code-block:: bash

   OPNSENSE_HOST=192.168.1.1 \
   OPNSENSE_API_KEY=your-key \
   OPNSENSE_API_SECRET=your-secret \
     poetry run pytest -m integration

Linting and type checking
--------------------------

.. code-block:: bash

   poetry run ruff check .
   poetry run mypy opnsense_py/

Adding a new module
-------------------

1. Create ``opnsense_py/models/<name>.py`` with Pydantic models for the
   resource.  Extend :class:`~opnsense_py.models.base.OPNsenseModel`.

2. Create ``opnsense_py/modules/core/<name>.py`` (or ``plugins/``) with a
   class extending :class:`~opnsense_py.modules.base.BaseModule`.  Delegate to
   the inherited CRUD helpers.

3. Add a ``@cached_property`` accessor to ``OPNsenseClient`` in
   ``opnsense_py/client.py``.

4. Export the new module class in ``opnsense_py/__init__.py`` if needed.

5. Add tests in ``tests/unit/modules/core/test_<name>.py`` using the
   ``client`` and ``mock_api`` fixtures from ``tests/conftest.py``.

See ``opnsense_py/modules/core/cron.py`` and ``tests/unit/modules/core/test_cron.py``
for a reference implementation.

Testing CLI commands
--------------------

CLI commands are tested by injecting a pre-built ``_LazyContext`` (with a
``respx``-mocked client) via ``runner.invoke``:

.. code-block:: python

   def test_list_jobs(runner, cli_obj, mock_api):
       mock_api.post("cron/settings/search_jobs").mock(
           return_value=httpx.Response(200, json={...})
       )
       result = runner.invoke(cli, ["cron", "list-jobs"], obj=cli_obj)
       assert result.exit_code == 0

See ``tests/unit/cli/conftest.py`` for the fixture pattern.

Building the docs
-----------------

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme sphinx-tabs sphinx-sitemap
   cd docs
   make html

The built docs will be in ``docs/_build/html/``.
