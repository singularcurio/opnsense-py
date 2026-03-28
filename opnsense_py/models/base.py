from __future__ import annotations

from typing import Any, Generic, TypeVar, get_args

from pydantic import BaseModel, ConfigDict, model_validator

T = TypeVar("T")


def _extract_selected(d: dict[str, Any]) -> str | None:
    """Return the key whose value dict has ``selected == 1``, or ``None``."""
    for key, meta in d.items():
        if isinstance(meta, dict) and meta.get("selected") == 1:
            return key
    return None


def _is_optional(annotation: Any, target: type) -> bool:
    """Return True if ``annotation`` is ``target | None`` / ``Optional[target]``."""
    args = get_args(annotation)
    return bool(args) and target in args and type(None) in args


class OPNsenseModel(BaseModel):
    """Base for all OPNsense models. Extra fields are silently accepted."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def _normalize_edit_form(cls, values: Any) -> Any:
        """Normalize the edit-form response format returned by OPNsense ``get_*`` endpoints.

        Edit-form responses differ from grid/search responses in two ways:
        - Dropdown/enum fields are dicts like ``{"A": {"value": "...", "selected": 1}, ...}``
          instead of plain strings.
        - Optional integer fields use ``""`` when unset instead of ``null``.

        This validator handles both cases generically for all subclasses.
        """
        if not isinstance(values, dict):
            return values
        for field_name, field_info in cls.model_fields.items():
            if field_name not in values:
                continue
            value = values[field_name]
            ann = field_info.annotation
            if _is_optional(ann, int) and value == "":
                values[field_name] = None
            elif _is_optional(ann, str) and isinstance(value, dict):
                values[field_name] = _extract_selected(value)
        return values


class SearchRequest(BaseModel):
    """Standard grid search request body."""

    current: int = 1
    rowCount: int = 500
    searchPhrase: str = ""
    sort: dict[str, str] = {}


class SearchResponse(BaseModel, Generic[T]):
    """Standard grid search response envelope."""

    total: int
    rowCount: int
    current: int
    rows: list[T]

    model_config = ConfigDict(extra="allow")


class ApiResponse(BaseModel):
    """Generic envelope for simple POST responses (result/uuid)."""

    result: str | None = None
    uuid: str | None = None
    validations: dict[str, Any] | None = None

    model_config = ConfigDict(extra="allow")
