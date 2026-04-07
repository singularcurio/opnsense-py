from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

import typer

from opnsense_py import OPNsenseClient

_CONFIG_PATH = Path.home() / ".config" / "opnsense-py" / "config.toml"


@dataclass
class CliContext:
    client: OPNsenseClient
    output_format: str  # "table" | "json" | "plain"


def _load_config_file(profile: str) -> dict[str, str]:
    """Load connection settings from the TOML config file for the given profile."""
    if not _CONFIG_PATH.exists():
        return {}
    with _CONFIG_PATH.open("rb") as f:
        data = tomllib.load(f)
    return {k: str(v) for k, v in data.get(profile, {}).items()}


def build_client(
    host: str | None,
    api_key: str | None,
    api_secret: str | None,
    verify_ssl: bool,
    https: bool,
    profile: str,
) -> OPNsenseClient:
    """Resolve connection settings via three-tier priority and return a client.

    Priority (highest wins): CLI flags > env vars > config file.
    """
    cfg = _load_config_file(profile)

    resolved_host = host or os.environ.get("OPNSENSE_HOST") or cfg.get("host")
    resolved_key = api_key or os.environ.get("OPNSENSE_API_KEY") or cfg.get("api_key")
    resolved_secret = (
        api_secret or os.environ.get("OPNSENSE_API_SECRET") or cfg.get("api_secret")
    )

    # verify_ssl: CLI flag (--no-verify-ssl sets it to False) takes precedence, then env, then config
    env_verify = os.environ.get("OPNSENSE_VERIFY_SSL")
    if not verify_ssl:
        resolved_verify = False
    elif env_verify is not None:
        resolved_verify = env_verify.lower() not in ("0", "false", "no")
    else:
        cfg_verify = cfg.get("verify_ssl", "true")
        resolved_verify = cfg_verify.lower() not in ("0", "false", "no")

    # https: CLI flag (--no-tls) takes precedence, then env, then config
    if not https:
        resolved_https = False
    else:
        env_https = os.environ.get("OPNSENSE_HTTPS")
        if env_https is not None:
            resolved_https = env_https.lower() not in ("0", "false", "no")
        else:
            cfg_https = cfg.get("https", "true")
            resolved_https = cfg_https.lower() not in ("0", "false", "no")

    missing = [
        name
        for name, val in [
            ("host", resolved_host),
            ("api-key", resolved_key),
            ("api-secret", resolved_secret),
        ]
        if not val
    ]
    if missing:
        raise typer.BadParameter(
            f"Missing required connection setting(s): {', '.join(missing)}. "
            f"Provide via --{missing[0]}, OPNSENSE_{missing[0].upper().replace('-', '_')} env var, "
            f"or ~/.config/opnsense-py/config.toml."
        )

    return OPNsenseClient(
        host=resolved_host,  # type: ignore[arg-type]
        api_key=resolved_key,  # type: ignore[arg-type]
        api_secret=resolved_secret,  # type: ignore[arg-type]
        verify_ssl=resolved_verify,
        https=resolved_https,
    )
