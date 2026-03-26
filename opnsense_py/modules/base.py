from __future__ import annotations

from typing import TYPE_CHECKING, Any

from opnsense_py.models.base import ApiResponse, SearchRequest, SearchResponse

if TYPE_CHECKING:
    from opnsense_py.client import OPNsenseClient


class BaseModule:
    """Base class for all OPNsense API modules."""

    def __init__(self, client: OPNsenseClient) -> None:
        self._client = client

    # ------------------------------------------------------------------
    # CRUD helpers
    # ------------------------------------------------------------------

    def _search(
        self,
        module: str,
        controller: str,
        command: str,
        request: SearchRequest | None = None,
    ) -> SearchResponse[dict[str, Any]]:
        """POST a grid-search request and return one page of results."""
        req = request or SearchRequest()
        raw = self._client._post(
            f"{module}/{controller}/{command}", json=req.model_dump()
        )
        return SearchResponse[dict[str, Any]].model_validate(raw)

    def _search_all(
        self,
        module: str,
        controller: str,
        command: str,
        search_phrase: str = "",
        sort: dict[str, str] | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch all rows, paginating automatically if needed."""
        req = SearchRequest(
            current=1, rowCount=500, searchPhrase=search_phrase, sort=sort or {}
        )
        first = self._search(module, controller, command, req)
        rows = list(first.rows)

        if first.total <= len(rows):
            return rows

        page = 2
        while len(rows) < first.total:
            req = SearchRequest(
                current=page, rowCount=500, searchPhrase=search_phrase, sort=sort or {}
            )
            page_data = self._search(module, controller, command, req)
            if not page_data.rows:
                break
            rows.extend(page_data.rows)
            page += 1

        return rows

    def _get_item(
        self,
        module: str,
        controller: str,
        command: str,
        uuid: str | None = None,
    ) -> dict[str, Any]:
        """GET a single item, optionally scoped to *uuid*."""
        path = f"{module}/{controller}/{command}"
        if uuid:
            path = f"{path}/{uuid}"
        return self._client._get(path)

    def _add_item(
        self,
        module: str,
        controller: str,
        command: str,
        data: dict[str, Any],
    ) -> ApiResponse:
        """POST *data* to create a new item; returns the new UUID in ``ApiResponse.uuid``."""
        raw = self._client._post(f"{module}/{controller}/{command}", json=data)
        return ApiResponse.model_validate(raw)

    def _set_item(
        self,
        module: str,
        controller: str,
        command: str,
        uuid: str,
        data: dict[str, Any],
    ) -> ApiResponse:
        """POST *data* to update an existing item identified by *uuid*."""
        raw = self._client._post(f"{module}/{controller}/{command}/{uuid}", json=data)
        return ApiResponse.model_validate(raw)

    def _del_item(
        self,
        module: str,
        controller: str,
        command: str,
        uuid: str,
    ) -> ApiResponse:
        """POST to delete the item identified by *uuid*."""
        raw = self._client._post(f"{module}/{controller}/{command}/{uuid}")
        return ApiResponse.model_validate(raw)

    def _toggle_item(
        self,
        module: str,
        controller: str,
        command: str,
        uuid: str,
        enabled: bool | None = None,
    ) -> ApiResponse:
        """Toggle the enabled state of *uuid*. Pass *enabled* to force a specific state."""
        path = f"{module}/{controller}/{command}/{uuid}"
        if enabled is not None:
            path = f"{path}/{int(enabled)}"
        raw = self._client._post(path)
        return ApiResponse.model_validate(raw)

    # ------------------------------------------------------------------
    # Config get/set helpers
    # ------------------------------------------------------------------

    def _get_config(self, module: str, controller: str) -> dict[str, Any]:
        return self._client._get(f"{module}/{controller}/get")

    def _set_config(
        self, module: str, controller: str, data: dict[str, Any]
    ) -> ApiResponse:
        raw = self._client._post(f"{module}/{controller}/set", json=data)
        return ApiResponse.model_validate(raw)

    # ------------------------------------------------------------------
    # Service control helpers
    # ------------------------------------------------------------------

    def _service_start(self, module: str) -> ApiResponse:
        return ApiResponse.model_validate(self._client._post(f"{module}/service/start"))

    def _service_stop(self, module: str) -> ApiResponse:
        return ApiResponse.model_validate(self._client._post(f"{module}/service/stop"))

    def _service_restart(self, module: str) -> ApiResponse:
        return ApiResponse.model_validate(
            self._client._post(f"{module}/service/restart")
        )

    def _service_reconfigure(self, module: str) -> ApiResponse:
        return ApiResponse.model_validate(
            self._client._post(f"{module}/service/reconfigure")
        )

    def _service_status(self, module: str) -> dict[str, Any]:
        return self._client._get(f"{module}/service/status")
