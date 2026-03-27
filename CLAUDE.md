# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install with CLI extras
pip install opnsense-py[cli]   # or: uv sync --extra cli

# Run tests (excludes integration tests by default)
uv run pytest

# Run a single test file
uv run pytest tests/unit/modules/core/test_cron.py

# Run a single test
uv run pytest tests/unit/modules/core/test_cron.py::test_search_jobs

# Run integration tests (requires live OPNsense instance)
uv run pytest -m integration

# Lint
uv run ruff check .

# Type check
uv run mypy opnsense_py/
```

## Architecture

**opnsense-py** is a synchronous Python client library for the OPNsense REST API using `httpx` and `pydantic`.

### Layers

1. **`OPNsenseClient`** (`client.py`) — top-level entry point. Manages an `httpx.Client` with Basic Auth. All API modules are lazy-loaded as `@cached_property` attributes (e.g., `client.cron`, `client.firewall`). Low-level `_get()` / `_post()` methods handle HTTP and raise typed exceptions.

2. **`BaseModule`** (`modules/base.py`) — base class for all module wrappers. Provides generic CRUD helpers (`_search()`, `_search_all()`, `_get_item()`, `_add_item()`, `_set_item()`, `_del_item()`, `_toggle_item()`) and service control helpers (`_service_reconfigure()`, etc.). All module methods delegate to these.

3. **Module classes** (`modules/core/`, `modules/plugins/`) — one class per OPNsense subsystem (e.g., `CronModule`, `FirewallModule`, `UnboundModule`). They wrap specific API endpoints and return typed Pydantic models.

4. **Pydantic models** (`models/`) — typed representations of OPNsense entities. `models/base.py` defines shared types: `OPNsenseModel` (base with `extra="allow"`), `SearchRequest`, `SearchResponse[T]`, and `ApiResponse`.

5. **Exceptions** (`exceptions.py`) — `OPNsenseError` → `OPNsenseHTTPError` → `OPNsenseAuthError` / `OPNsenseNotFoundError`; separate `OPNsenseValidationError` for HTTP 200 responses that carry validation error payloads.

### CLI (`opnsense_py/cli/`)

The `opn` / `opnsense` binary is a Click CLI layered over the library.

- **`context.py`** — `build_client()` resolves connection settings via three-tier priority: config file (`~/.config/opnsense-py/config.toml`) → env vars (`OPNSENSE_HOST`, `OPNSENSE_API_KEY`, `OPNSENSE_API_SECRET`, `OPNSENSE_VERIFY_SSL`, `OPNSENSE_PROFILE`) → CLI flags (`--host`, `--api-key`, etc.). `_LazyContext` defers client construction until the first command accesses `.client`.
- **`output.py`** — `render(data, fmt)` renders `SearchResponse`, `ApiResponse`, or any `OPNsenseModel` as `table` (default, via `tabulate`), `json`, or `plain` (UUIDs/values one per line for piping).
- **`main.py`** — Root `cli` group with shared flags and an `handle_api_errors` decorator that maps the exception hierarchy to clean messages and distinct exit codes (2=auth, 3=not found, 4=validation).
- **`commands/cron.py`** — Reference implementation of a full-CRUD command group (`list-jobs`, `get-job`, `add-job`, `set-job`, `del-job`, `toggle-job`, `reconfigure`). All `add-*`/`set-*` commands accept individual `--field` flags or `--from-json FILE|-` for complex payloads.

**Testing CLI commands**: inject a pre-built `_LazyContext` (with a `respx`-mocked client) via `runner.invoke(cli, args, obj=cli_obj)`. The root group skips creating a new context when it detects an existing `_LazyContext` in `ctx.obj`. See `tests/unit/cli/conftest.py` for the fixture pattern.

### Adding a new module

1. Create `opnsense_py/models/<name>.py` with Pydantic models for the resource.
2. Create `opnsense_py/modules/core/<name>.py` (or `plugins/`) with a class extending `BaseModule`. Call the inherited helpers.
3. Add a `@cached_property` accessor to `OPNsenseClient` in `client.py`.
4. Export the new module in `opnsense_py/__init__.py` if needed.
5. Add tests in `tests/unit/modules/core/test_<name>.py` using the `client` and `mock_api` fixtures from `conftest.py`.

### Testing approach

Tests use `respx` to mock `httpx` at the transport level. The `mock_api` fixture (in `tests/conftest.py`) creates a `respx.MockRouter` scoped to `https://opnsense.test:443`. The `client` fixture returns an `OPNsenseClient` pointed at that host. Tests register expected routes on `mock_api` and assert on parsed return values or raised exceptions.
