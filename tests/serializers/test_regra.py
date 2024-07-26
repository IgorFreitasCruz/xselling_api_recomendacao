"""Test module for Regra serializer"""
import json

from src.domain.regra import Regra
from src.serializers.regra import RegraJsonEncoder


def test_serialize_domain_client():
    regra = Regra(
        regra_id=1,
        confianca=30.0,
        suporte=3.0,
        lift=5.0,
        antecedentes=[1, 2, 3, 4],
        consequentes=[1, 2, 3, 4],
    )

    excepted_json = """
        {
            "regra_id": 1,
            "confianca": 30.0,
            "suporte": 3.0,
            "lift": 5.0,
            "antecedentes": [1, 2, 3, 4],
            "consequentes": [1, 2, 3, 4]
        }
        """

    json_regra = json.dumps(regra, cls=RegraJsonEncoder)

    assert json.loads(json_regra) == json.loads(excepted_json)
