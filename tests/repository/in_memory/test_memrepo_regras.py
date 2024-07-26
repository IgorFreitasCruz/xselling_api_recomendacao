import pytest

from src.domain.regra import Regra
from src.repository.in_memory.memrepo_cache import MemRepoCache


@pytest.fixture
def regras_cache():
    return [
        {
            'regra_id': 1,
            'confianca': 30.0,
            'suporte': 3.0,
            'lift': 5.0,
            'antecedentes': [1, 2, 3, 4],
            'consequentes': [3, 4],
        },
        {
            'regra_id': 2,
            'confianca': 30.0,
            'suporte': 3.0,
            'lift': 5.0,
            'antecedentes': [1, 2, 3, 4],
            'consequentes': [3, 4],
        },
        {
            'regra_id': 3,
            'confianca': 30.0,
            'suporte': 3.0,
            'lift': 5.0,
            'antecedentes': [3, 4],
            'consequentes': [1, 2],
        },
        {
            'regra_id': 4,
            'confianca': 30.0,
            'suporte': 3.0,
            'lift': 5.0,
            'antecedentes': [3, 4],
            'consequentes': [1, 2],
        },
    ]


def test_regra_repository_set(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_regras()

    assert len(result) == 4


def test_regra_repository_get(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    assert repo._obter_regras() == [Regra.from_dict(r) for r in regras_cache]


def test_regra_repository_get_by_antecedentes_ids(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_regras_por_antecedentes(categoria_ids=[3, 4])

    assert len(result) == 2


def test_regra_repository_get_by_consequentes_ids(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_consequentes_por_regra(regra_ids=[3, 4])

    assert len(result) == 2


def test_regra_repository_filter_by_regra_id(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_regras(filters={'regra_id__eq': 1})

    assert len(result) == 1
    assert result[0].regra_id == 1


def test_regra_repository_filter_by_regra_ids(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_regras(filters={'regra_id__in': [1, 2]})

    assert len(result) == 2


def test_regra_repository_filter_by_antecedente_ids(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_regras(filters={'antecedentes_ids__eq': [3, 4]})

    assert len(result) == 2


def test_regra_repository_filter_by_consequente_ids(regras_cache):
    repo = MemRepoCache()
    repo._set_cache_regras_ia(regras_cache)

    result = repo._obter_regras(filters={'consequentes_ids__eq': [1, 2]})

    assert len(result) == 2
