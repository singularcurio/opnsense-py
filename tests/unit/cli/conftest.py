import pytest
import respx
from typer.testing import CliRunner

from opnsense_py import OPNsenseClient
from opnsense_py.cli.main import _LazyContext


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def mock_api():
    with respx.mock(base_url="https://opnsense.test:443", assert_all_called=False) as mock:
        yield mock


@pytest.fixture
def cli_client(mock_api: respx.MockRouter) -> OPNsenseClient:
    return OPNsenseClient(
        host="opnsense.test",
        api_key="testkey",
        api_secret="testsecret",
        verify_ssl=False,
    )


@pytest.fixture
def cli_obj(cli_client: OPNsenseClient) -> _LazyContext:
    """A pre-built _LazyContext that injects the mocked client."""
    ctx = _LazyContext(
        host=None,
        api_key=None,
        api_secret=None,
        verify_ssl=False,
        https=True,
        profile="default",
        output_format="table",
    )
    ctx._client = cli_client
    return ctx
