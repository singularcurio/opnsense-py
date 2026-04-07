import httpx
import respx
from typer.testing import CliRunner

from opnsense_py.cli.main import app
from opnsense_py.cli.main import _LazyContext


def _invoke(runner: CliRunner, cli_obj: _LazyContext, args: list[str]):
    return runner.invoke(app, args, obj=cli_obj, catch_exceptions=False)


# ---------------------------------------------------------------------------
# list-jobs
# ---------------------------------------------------------------------------


def test_list_jobs_table(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/cron/settings/search_jobs").mock(
        return_value=httpx.Response(
            200,
            json={
                "total": 1,
                "rowCount": 1,
                "current": 1,
                "rows": [{"uuid": "abc-1", "description": "nightly"}],
            },
        )
    )
    result = _invoke(runner, cli_obj, ["cron", "list-jobs"])
    assert result.exit_code == 0
    assert "abc-1" in result.output
    assert "nightly" in result.output


def test_list_jobs_json(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    cli_obj.output_format = "json"
    mock_api.post("/api/cron/settings/search_jobs").mock(
        return_value=httpx.Response(
            200,
            json={"total": 1, "rowCount": 1, "current": 1, "rows": [{"uuid": "abc-1"}]},
        )
    )
    result = _invoke(runner, cli_obj, ["cron", "list-jobs"])
    assert result.exit_code == 0
    import json
    data = json.loads(result.output)
    assert data["rows"][0]["uuid"] == "abc-1"


def test_list_jobs_plain_uuids(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    cli_obj.output_format = "plain"
    mock_api.post("/api/cron/settings/search_jobs").mock(
        return_value=httpx.Response(
            200,
            json={
                "total": 2,
                "rowCount": 2,
                "current": 1,
                "rows": [{"uuid": "abc-1"}, {"uuid": "abc-2"}],
            },
        )
    )
    result = _invoke(runner, cli_obj, ["cron", "list-jobs"])
    assert result.exit_code == 0
    assert result.output.strip().splitlines() == ["abc-1", "abc-2"]


# ---------------------------------------------------------------------------
# get-job
# ---------------------------------------------------------------------------


def test_get_job(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    mock_api.get("/api/cron/settings/get_job/abc-1").mock(
        return_value=httpx.Response(200, json={"job": {"description": "nightly", "command": "/bin/run"}})
    )
    result = _invoke(runner, cli_obj, ["cron", "get-job", "abc-1"])
    assert result.exit_code == 0
    assert "nightly" in result.output


# ---------------------------------------------------------------------------
# add-job
# ---------------------------------------------------------------------------


def test_add_job_with_flags(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/cron/settings/add_job").mock(
        return_value=httpx.Response(200, json={"result": "saved", "uuid": "new-uuid"})
    )
    result = _invoke(
        runner,
        cli_obj,
        ["cron", "add-job", "--command", "/bin/true", "--description", "test"],
    )
    assert result.exit_code == 0
    assert route.called
    assert "saved" in result.output


def test_add_job_with_json_stdin(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/cron/settings/add_job").mock(
        return_value=httpx.Response(200, json={"result": "saved", "uuid": "new-uuid"})
    )
    result = runner.invoke(
        app,
        ["cron", "add-job", "--from-json", "-"],
        obj=cli_obj,
        input='{"command": "/bin/echo", "description": "from stdin"}',
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "saved" in result.output


# ---------------------------------------------------------------------------
# del-job
# ---------------------------------------------------------------------------


def test_del_job(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/cron/settings/del_job/abc-1").mock(
        return_value=httpx.Response(200, json={"result": "deleted"})
    )
    result = _invoke(runner, cli_obj, ["cron", "del-job", "abc-1"])
    assert result.exit_code == 0
    assert route.called
    assert "deleted" in result.output


# ---------------------------------------------------------------------------
# toggle-job
# ---------------------------------------------------------------------------


def test_toggle_job_no_flag(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/cron/settings/toggle_job/abc-1").mock(
        return_value=httpx.Response(200, json={"result": "saved"})
    )
    result = _invoke(runner, cli_obj, ["cron", "toggle-job", "abc-1"])
    assert result.exit_code == 0
    assert route.called


def test_toggle_job_disable(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/cron/settings/toggle_job/abc-1/0").mock(
        return_value=httpx.Response(200, json={"result": "saved"})
    )
    result = _invoke(runner, cli_obj, ["cron", "toggle-job", "abc-1", "--disable"])
    assert result.exit_code == 0
    assert route.called


# ---------------------------------------------------------------------------
# reconfigure
# ---------------------------------------------------------------------------


def test_reconfigure(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    route = mock_api.post("/api/cron/service/reconfigure").mock(
        return_value=httpx.Response(200, json={"result": "ok"})
    )
    result = _invoke(runner, cli_obj, ["cron", "reconfigure"])
    assert result.exit_code == 0
    assert route.called


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def test_auth_error_exits_2(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/cron/settings/search_jobs").mock(
        return_value=httpx.Response(401, text="Unauthorized")
    )
    result = runner.invoke(app, ["cron", "list-jobs"], obj=cli_obj)
    assert result.exit_code == 2


def test_not_found_exits_3(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    mock_api.get("/api/cron/settings/get_job/missing").mock(
        return_value=httpx.Response(404, text="Not Found")
    )
    result = runner.invoke(app, ["cron", "get-job", "missing"], obj=cli_obj)
    assert result.exit_code == 3


def test_validation_error_exits_4(
    runner: CliRunner, cli_obj: _LazyContext, mock_api: respx.MockRouter
) -> None:
    mock_api.post("/api/cron/settings/add_job").mock(
        return_value=httpx.Response(
            200,
            json={
                "result": "failed",
                "validations": {"job.command": "This field is required."},
            },
        )
    )
    result = runner.invoke(app, ["cron", "add-job"], obj=cli_obj)
    assert result.exit_code == 4
    assert "job.command" in result.output
