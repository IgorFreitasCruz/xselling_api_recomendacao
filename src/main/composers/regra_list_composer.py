from src.presentation.controllers.regra_list_controller import (
    RegraListController,
)
from src.repository.in_memory.memrepo_cache import MemRepoCache
from src.use_cases.regra_list import RegraListUseCase

data = [
    {
        'regra_id': 1,
        'confianca': 30.0,
        'suporte': 3.0,
        'antecedentes': [1, 2, 3, 4],
        'consequentes': [1, 2, 3, 4],
    },
    {
        'regra_id': 2,
        'confianca': 30.0,
        'suporte': 3.0,
        'antecedentes': [1, 2, 3, 4],
        'consequentes': [1, 2, 3, 4],
    },
    {
        'regra_id': 3,
        'confianca': 30.0,
        'suporte': 3.0,
        'antecedentes': [3, 4],
        'consequentes': [1, 2],
    },
    {
        'regra_id': 4,
        'confianca': 30.0,
        'suporte': 3.0,
        'antecedentes': [3, 4],
        'consequentes': [1, 2],
    },
]


def regra_list_composer():
    repository = MemRepoCache()
    repository._set_cache_regras_ia(data)
    regra_use_case = RegraListUseCase(regra_repository=repository)
    controller = RegraListController(use_case=regra_use_case)

    return controller.handle
