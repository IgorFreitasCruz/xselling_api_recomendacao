from abc import ABC, abstractmethod


class CacheInterface(ABC):
    @abstractmethod
    def _set_cache_regras_ia(self, data: list[dict]):
        raise NotImplementedError

    @abstractmethod
    def _obter_regras(self, filters: dict = None):
        raise NotImplementedError

    @abstractmethod
    def _obter_regras_por_antecedentes(self, categoria_ids: list[int]):
        raise NotImplementedError
