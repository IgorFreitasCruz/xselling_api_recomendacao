import pytest

from src.presentation.http_types.http_response import HttpResponse

result = {
    'type': 'Recomendacao',
    'count': 1,
    'attributes': [{}],
}


@pytest.mark.asyncio
async def test_valid_request_received(mocker, client):
    # Arrange

    mocker.patch(
        'src.main.rest.recomendacao.request_adapter',
        return_value=HttpResponse(status_code=200, body={}),
    )
    # mocker.patch('src.main.recomendacao_list.handle_errors', return_value=HttpResponse(status_code=500, body={}))

    # Act
    response = client.post(
        '/regras-ia-recomendacao', json={'produtos': [1, 2, 3]}
    )

    # Assert
    assert response.status_code == 200


@pytest.mark.skip('olhar depois')
@pytest.mark.asyncio
async def test_calls_recomendacao_list_composer(mocker, client):
    # Arrange

    # Act
    mock_composer = mocker.patch(
        'src.main.rest.recomendacao.recomendacao_list_composer',
        return_value=HttpResponse(status_code=200, body={}),
    )

    response = client.post(
        '/regras-ia-recomendacao', json={'produto': [1, 2, 3]}
    )

    # Assert
    mock_composer.assert_called_once()
    assert response.status_code == 200
