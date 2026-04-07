from __future__ import annotations

import json
import sys
from typing import Any, Type, TypeVar

import typer
from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


def build_model(model_cls: Type[M], from_json: str | None, **fields: Any) -> M:
    """Construct a Pydantic model from --from-json or individual field flags.

    If *from_json* is given it takes precedence; field flags are ignored.
    Use '-' to read from stdin.
    """
    if from_json is not None:
        if from_json == "-":
            raw = sys.stdin.read()
        else:
            try:
                with open(from_json) as f:
                    raw = f.read()
            except OSError as exc:
                raise typer.BadParameter(str(exc), param_hint="--from-json") from exc
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"Invalid JSON: {exc}", param_hint="--from-json") from exc
        return model_cls.model_validate(data)
    return model_cls(**{k: v for k, v in fields.items() if v is not None})


def require_confirmation(yes: bool, action: str = "this action") -> None:
    """Raise BadParameter if --yes was not passed for a destructive command."""
    if not yes:
        raise typer.BadParameter(
            f"Pass --yes to confirm {action}.",
            param_hint="--yes",
        )
