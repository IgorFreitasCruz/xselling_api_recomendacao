import json

from src.domain.regra import Regra


def test_regras_model_init():
    regra = Regra(
        regra_id=1,
        confianca=30.0,
        suporte=3.0,
        lift=5.0,
        antecedentes=[1, 2, 3, 4],
        consequentes=[1, 2, 3, 4],
    )

    assert regra.regra_id == 1
    assert regra.confianca == 30.0
    assert regra.suporte == 3.0
    assert regra.lift == 5.0
    assert regra.antecedentes == [1, 2, 3, 4]
    assert regra.consequentes == [1, 2, 3, 4]


def test_regras_model_from_dict():
    init_dict = {
        'regra_id': 1,
        'confianca': 30.0,
        'suporte': 3.0,
        'lift': 5.0,
        'antecedentes': [1, 2, 3, 4],
        'consequentes': [1, 2, 3, 4],
    }

    regra = Regra.from_dict(init_dict)

    assert regra.regra_id == 1
    assert regra.confianca == 30.0
    assert regra.suporte == 3.0
    assert regra.lift == 5.0
    assert regra.antecedentes == [1, 2, 3, 4]
    assert regra.consequentes == [1, 2, 3, 4]


def test_regras_model_to_dict():
    init_dict = {
        'regra_id': 1,
        'confianca': 30.0,
        'suporte': 3.0,
        'lift': 5.0,
        'antecedentes': [1, 2, 3, 4],
        'consequentes': [1, 2, 3, 4],
    }

    regra = Regra.from_dict(init_dict)

    assert regra.to_dict() == init_dict


def test_regras_model_from_json():
    init_dict = {
        'regra_id': 1,
        'confianca': 30.0,
        'suporte': 3.0,
        'lift': 5.0,
        'antecedentes': [1, 2, 3, 4],
        'consequentes': [1, 2, 3, 4],
    }

    regra = Regra.from_json(json.dumps(init_dict))

    assert Regra.from_dict(init_dict) == regra


def test_regras_model_to_json():
    init_dict = {
        'regra_id': 1,
        'confianca': 30.0,
        'suporte': 3.0,
        'lift': 5.0,
        'antecedentes': [1, 2, 3, 4],
        'consequentes': [1, 2, 3, 4],
    }

    regra = Regra.from_dict(init_dict)

    json_data = regra.to_json()

    assert Regra.from_json(json_data) == Regra.from_dict(init_dict)
