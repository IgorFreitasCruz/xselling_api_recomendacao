from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import (
    HttpResponse,
    HttpStatusCode,
)
from src.presentation.interfaces.controller_interface import (
    ControllerInterface,
)
from src.use_cases.regra_list import RegraListUseCase


class RegraListController(ControllerInterface):
    def __init__(self, use_case: RegraListUseCase):
        self._use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        result: list = self._use_case.execute(request=http_request.json)

        return HttpResponse(status_code=HttpStatusCode.OK, body=result)
