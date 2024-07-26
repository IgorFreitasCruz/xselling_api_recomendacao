import dataclasses


@dataclasses.dataclass
class Recomendacao:
    """Recomendacao entity"""

    cliente_id: int
    produto_ids: list[int]

    @classmethod
    def from_dict(cls, d):
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
