from src.drivers.jwt_plugin import auth_token
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import (
    HttpResponse,
    HttpStatusCode,
)
from src.presentation.interfaces.controller_interface import (
    ControllerInterface,
)
from src.use_cases.recomendacao_list import RecomendacaoListUseCase


class RecomendacaoListController(ControllerInterface):
    def __init__(self, use_case: RecomendacaoListUseCase):
        self._use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        client: dict = auth_token.validate_token(http_request=http_request)

        result: list[dict] = self._use_case.execute(
            http_request=http_request.json, client=client
        )

        return HttpResponse(status_code=HttpStatusCode.OK.value, body=result)
