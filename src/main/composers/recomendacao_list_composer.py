from src.presentation.controllers.recomendacao_list_controller import (
    RecomendacaoListController,
)
from src.use_cases.recomendacao_list import RecomendacaoListUseCase


def recomendacao_list_composer():

    recomendacao_use_case = RecomendacaoListUseCase()

    controller = RecomendacaoListController(recomendacao_use_case)

    return controller.handle
