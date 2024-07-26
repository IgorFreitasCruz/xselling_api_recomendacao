import pytest
from fastapi.testclient import TestClient

from src.main.server.app import create_app


@pytest.fixture
def client():
    """Factory for application

    Returns:
        Object: Application configuration
    """
    app = create_app()

    client = TestClient(app)

    return client


def pytest_addoption(parser):
    """Hook into the pytest CLI parser that adds the option --integration
    When the 'integration' option is specified on the command line the pytest
    setup will contain the key integration with value True

    Args:
        parser (Object): Pytest CLI parser object
    """
    parser.addoption(
        '--integration', action='store_true', help='run integrations tests'
    )


def pytest_runtest_setup(item):
    """Hook into the pytest setup of every single test
    The attribute item.config contains the parsed pytest command line.

    If the test is marked with integration ('integration' in item.keywords) and
    the option --integration is not present (not item.config.getvalue("integration"))
    the test is skipped.

    Args:
        item (Object): Pytest CLI item object
    """
    if 'integration' in item.keywords and not item.config.getvalue(
        'integration'
    ):
        pytest.skip('need --integration option to run')
