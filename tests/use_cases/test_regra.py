from unittest.mock import Mock

import pytest

from src.domain.regra import Regra
from src.errors.types import NotFoundError
from src.repository.in_memory.memrepo_cache import MemRepoCache
from src.use_cases.regra_list import RegraListUseCase


@pytest.fixture
def mock_repo():
    return Mock(spec=MemRepoCache)


@pytest.fixture
def use_case(mock_repo):
    return RegraListUseCase(regra_repository=mock_repo)


def test_execute(use_case, mock_repo):
    # Prepare data for the test
    request_data = {'produtos': [{'categoria_id': 1}, {'categoria_id': 2}]}

    # Mock the repository method to return some data
    mock_repo._obter_regras_por_antecedentes.return_value = [
        Regra(
            regra_id=1,
            confianca=30.0,
            suporte=3.0,
            lift=5.0,
            antecedentes=[1, 2, 3],
            consequentes=[4, 5, 6],
        )
    ]

    # Call the method under test
    result = use_case.execute(request=request_data)

    # Assertions
    assert 'type' in result
    assert 'count' in result
    assert 'attributes' in result


def test_execute_raises_not_found_error(use_case, mock_repo):
    # Prepare data for the test
    request_data = {'produtos': [{'categoria_id': 1}, {'categoria_id': 2}]}

    # Mock the repository method to return an empty list
    mock_repo._obter_regras_por_antecedentes.return_value = []

    # Call the method under test
    with pytest.raises(NotFoundError):
        use_case.execute(request=request_data)


def test_format_request():
    # Prepare data for the test
    request_data = {'produtos': [{'categoria_id': 1}, {'categoria_id': 2}]}

    # Call the static method under test
    result = RegraListUseCase._RegraListUseCase__format_request(request_data)

    # Assertions
    assert isinstance(result, list)
    assert result == [1, 2]


def test_search_regra(use_case, mock_repo):
    # Prepare data for the test
    categoria_ids = [1, 2]

    # Mock the repository method to return some data
    mock_repo._obter_regras_por_antecedentes.return_value = [
        Regra(
            regra_id=1,
            confianca=30.0,
            suporte=3.0,
            lift=5.0,
            antecedentes=[1, 2, 3],
            consequentes=[4, 5, 6],
        )
    ]

    # Call the method under test
    result = use_case._RegraListUseCase__search_regra(categoria_ids)

    # Assertions
    assert isinstance(result, list)
    assert len(result) == 1


def test_search_regra_raises_not_found_error(use_case, mock_repo):
    # Prepare data for the test
    categoria_ids = [1, 2]

    # Mock the repository method to return an empty list
    mock_repo._obter_regras_por_antecedentes.return_value = []

    # Call the method under test
    with pytest.raises(NotFoundError, match='Regra não encontrada'):
        use_case._RegraListUseCase__search_regra(categoria_ids)


def test_format_response():
    # Prepare data for the test
    regras = [
        Regra(
            regra_id=1,
            confianca=30.0,
            suporte=3.0,
            lift=5.0,
            antecedentes=[1, 2, 3],
            consequentes=[4, 5, 6],
        ),
        Regra(
            regra_id=2,
            confianca=30.0,
            suporte=3.0,
            lift=5.0,
            antecedentes=[1, 2, 3],
            consequentes=[4, 5, 6],
        ),
    ]

    # Call the static method under test
    result = RegraListUseCase._RegraListUseCase__format_response(regras)

    # Assertions
    assert 'type' in result
    assert 'count' in result
    assert 'attributes' in result
    assert result['count'] == len(regras)
    assert result['attributes'] == regras
