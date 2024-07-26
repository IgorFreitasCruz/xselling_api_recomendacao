import dataclasses
import json
from typing import Dict

from src.serializers.regra import RegraJsonEncoder


@dataclasses.dataclass
class Regra:
    """Regras entity"""

    regra_id: int
    confianca: float
    suporte: float
    lift: float
    antecedentes: list[int]
    consequentes: list[int]

    @classmethod
    def from_dict(cls, d: Dict):
        """Initialize an object from a dictionary

        Args:
            d (Dict): dictionary containing all class attributes

        Returns:
            Model: Instance of class object
        """
        return cls(**d)

    def to_dict(self):
        """Returns a dictionary from a class object

        Returns:
            Dict: dictionary containg all class attribute data
        """
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, d: str):
        """Initialize an object from a string

        Args:
            d (str): json containing all class attributes

        Returns:
            Model: Instance of class object
        """
        return cls(**json.loads(d))

    def to_json(self):
        """Returns a dictionary from a class object

        Returns:
            str: json containg all class attribute data
        """
        return json.dumps(self, cls=RegraJsonEncoder)
