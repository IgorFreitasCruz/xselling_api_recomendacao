from src.presentation.controllers.recomendacao_list_controller import (
    RecomendacaoListController,
)
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


# should return a HttpResponse with status code 200 and a list of recommended products when a valid HttpRequest is passed
def test_valid_http_request(mocker):
    # Arrange
    use_case_mock = mocker.Mock()
    controller = RecomendacaoListController(use_case_mock)
    http_request = HttpRequest(json={'produtos': [1, 2, 3]})
    expected_response = HttpResponse(
        status_code=200, body=['product1', 'product2', 'product3']
    )
    use_case_mock.execute.return_value = ['product1', 'product2', 'product3']

    # Act
    response = controller.handle(http_request)

    # Assert
    assert response.status_code == expected_response.status_code
    assert response.body == expected_response.body
    use_case_mock.execute.assert_called_once_with(
        http_request=http_request.json
    )
