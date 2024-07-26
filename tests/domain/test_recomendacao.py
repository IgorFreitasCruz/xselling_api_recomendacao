from src.domain.recomendacao import Recomendacao


def test_recomendacao_model_init():
    recomendacao = Recomendacao(cliente_id=1, produto_ids=[1, 2, 3, 4, 5])

    assert recomendacao.cliente_id == 1
    assert recomendacao.produto_ids == [1, 2, 3, 4, 5]


def test_recomendacao_model_from_dict():
    init_dict = {'cliente_id': 1, 'produto_ids': [1, 2, 3, 4, 5]}

    recomendacao = Recomendacao.from_dict(init_dict)

    assert recomendacao.cliente_id == 1
    assert recomendacao.produto_ids == [1, 2, 3, 4, 5]


def test_recomendacao_model_to_dict():
    init_dict = {'cliente_id': 1, 'produto_ids': [1, 2, 3, 4, 5]}

    recomendacao = Recomendacao.from_dict(init_dict)

    assert recomendacao.to_dict() == init_dict
