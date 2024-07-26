import json
from typing import Any


class RegraJsonEncoder(json.JSONEncoder):
    """Serializer class for the regra model

    Args:
        json (object): JSONEncoder

    Returns:
        str: serialized object
    """

    def default(self, o: Any) -> Any:
        try:
            to_serialize = {
                'regra_id': o.regra_id,
                'confianca': o.confianca,
                'suporte': o.suporte,
                'lift': o.lift,
                'antecedentes': o.antecedentes,
                'consequentes': o.consequentes,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
