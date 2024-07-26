import pytest

from src.repository.in_memory.memrepo_recomendacao import MemRepoRecomendacao


@pytest.fixture
def produtos_list():
    return [
        {
            'id': 1,
            'code': '0000-0000-0000-0000-0000-0000',
            'nome': 'Produto A',
            'descricao': 'Descrição A',
            'sku': '123',
            'categoria_id': 1,
            'dt_inclusao': '01/01/2023 00:00:00',
            'dt_alteracao': '01/01/2023 00:00:00',
            'ativo': True,
        },
        {
            'id': 2,
            'code': '0000-0000-0000-0000-0000-0000',
            'nome': 'Produto B',
            'descricao': 'Descrição B',
            'sku': '123',
            'categoria_id': 2,
            'dt_inclusao': '01/01/2023 00:00:00',
            'dt_alteracao': '01/01/2023 00:00:00',
            'ativo': True,
        },
        {
            'id': 3,
            'code': '0000-0000-0000-0000-0000-0000',
            'nome': 'Produto C',
            'descricao': 'Descrição C',
            'sku': '456',
            'categoria_id': 3,
            'dt_inclusao': '01/01/2023 00:00:00',
            'dt_alteracao': '01/01/2023 00:00:00',
            'ativo': True,
        },
        {
            'id': 4,
            'code': '0000-0000-0000-0000-0000-0000',
            'nome': 'Produto D',
            'descricao': 'Descrição D',
            'sku': '456',
            'categoria_id': 4,
            'dt_inclusao': '01/01/2023 00:00:00',
            'dt_alteracao': '01/01/2023 00:00:00',
            'ativo': True,
        },
    ]


def test_recomendacao_repository_get_product(produtos_list):
    repo = MemRepoRecomendacao(produtos_list)

    produtos = ['123']

    result = repo._obter_categoria_by_produto(produto_sku=produtos)

    assert len(result) == 2


def test_produtos_by_consequentes(produtos_list):
    repo = MemRepoRecomendacao(produtos_list)

    consequente_ids = [2, 3]

    result = repo._obter_produto_recomendado(consequente_ids=consequente_ids)

    assert len(result) == 2
    assert result[0]['nome'] == 'Produto B'
    assert result[1]['nome'] == 'Produto C'
