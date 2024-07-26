import pytest

from src.errors.types import NotFoundError
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.postgresrepo_product import PostgresRepoProduct
from src.use_cases.recomendacao_list import RecomendacaoListUseCase


# should return a list of recommended products when given a valid request
def test_valid_request_returns_recommended_products(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = [7, 8, 9]
    recomendacao_repository._obter_produto_recomendado.return_value = [
        {'id': 1, 'name': 'Product 1'},
        {'id': 2, 'name': 'Product 2'},
        {'id': 3, 'name': 'Product 3'},
    ]

    # Execute the use case
    response = use_case.execute(http_request=request)

    # Assert the response
    assert response == {
        'type': 'Recomendacao',
        'count': 3,
        'attributes': [
            {'id': 1, 'name': 'Product 1'},
            {'id': 2, 'name': 'Product 2'},
            {'id': 3, 'name': 'Product 3'},
        ],
    }


# should return a formatted response with the correct count and attributes
def test_formatted_response_has_correct_count_and_attributes(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = [7, 8, 9]
    recomendacao_repository._obter_produto_recomendado.return_value = [
        {'id': 1, 'name': 'Product 1'},
        {'id': 2, 'name': 'Product 2'},
        {'id': 3, 'name': 'Product 3'},
    ]

    # Execute the use case
    response = use_case.execute(request)

    # Assert the response
    assert response == {
        'type': 'Recomendacao',
        'count': 3,
        'attributes': [
            {'id': 1, 'name': 'Product 1'},
            {'id': 2, 'name': 'Product 2'},
            {'id': 3, 'name': 'Product 3'},
        ],
    }


# should raise a NotFoundError when no categories are found for the input products
def test_no_categories_found_raises_not_found_error(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = []
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = [7, 8, 9]
    recomendacao_repository._obter_produto_recomendado.return_value = [
        {'id': 1, 'name': 'Product 1'},
        {'id': 2, 'name': 'Product 2'},
        {'id': 3, 'name': 'Product 3'},
    ]

    # Execute and assert the exception
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should return an empty list when no recommended products are found for the input consequents
def test_no_recommended_products_found_returns_empty_list(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = [7, 8, 9]
    recomendacao_repository._obter_produto_recomendado.return_value = []

    # Execute and assert the exception
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no categories are found for an empty list of input products
def test_no_categories_found_for_empty_list_of_products_raises_not_found_error(
    mocker,
):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': []}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = []
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = [7, 8, 9]
    recomendacao_repository._obter_produto_recomendado.return_value = [
        {'id': 1, 'name': 'Product 1'},
        {'id': 2, 'name': 'Product 2'},
        {'id': 3, 'name': 'Product 3'},
    ]

    # Execute and assert the exception
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no rules are found for the input categories
def test_no_rules_found_for_categories(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = []

    # Assert that NotFoundError is raised
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no consequents are found for the input rules
def test_no_consequents_found(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = []

    # Assert that NotFoundError is raised
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no recommended products are found for the input consequents
def test_no_recommended_products_found(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = []

    # Assert that NotFoundError is raised
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no rules are found for an empty list of input categories
def test_no_rules_found_for_empty_categories(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': []}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = []
    regra_repository._obter_regras_por_antecedentes.return_value = []

    # Execute and assert the NotFoundError
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no consequents are found for an empty list of input rules
def test_no_consequents_found_for_empty_input_rules(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = []

    # Assert that NotFoundError is raised
    with pytest.raises(NotFoundError):
        use_case.execute(request)


# should raise a NotFoundError when no recommended products are found for an empty list of input consequents
def test_empty_consequents_not_found_error(mocker):
    # Create instances of the repositories
    recomendacao_repository = mocker.Mock()
    regra_repository = mocker.Mock()

    # Create an instance of the use case
    use_case = RecomendacaoListUseCase(
        recomendacao_repository, regra_repository
    )

    # Prepare the request data
    request = {'produtos': [1, 2, 3]}

    # Mock the repository methods
    recomendacao_repository._obter_categoria_by_produto.return_value = [
        1,
        2,
        3,
    ]
    regra_repository._obter_regras_por_antecedentes.return_value = [4, 5, 6]
    regra_repository._obter_consequentes_por_regra.return_value = []
    recomendacao_repository._obter_produto_recomendado.return_value = []

    # Execute and assert the NotFoundError
    with pytest.raises(NotFoundError):
        use_case.execute(request)


def test_recomendacao():
    repo = RecomendacaoListUseCase(
        recomendacao_repository=PostgresRepoProduct(),
        repo_cache=RedisRepository(),
    )

    result = repo.execute(
        http_request={'produtos': ['17', '365']},
        client={'cnpj': '00.000.000/0000-01'},
    )

    import sys
    from pprint import pprint

    print(
        '*' * 10,
        __name__,
        ': line',
        sys._getframe().f_lineno,
        '*' * 10,
        flush=True,
    )
    pprint(result)
