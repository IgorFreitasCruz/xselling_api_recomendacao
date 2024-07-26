"""Test module for product postgres repository"""
# pylint: disable=c0116
# pylint: disable=w0613
import pytest

from src.repository.postgres.postgresrepo_product import PostgresRepoProduct

# The module attribute pytestmark labels every test in the module with the tag integration
pytestmark = pytest.mark.integration


def test_product_repository_list_without_parameters(
    app_configuration, pg_session
):
    repo = PostgresRepoProduct(app_configuration)

    products = repo.list_product()

    assert len(products) == 4
