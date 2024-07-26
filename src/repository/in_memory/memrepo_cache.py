import json

from src.domain.regra import Regra

from ..interfaces.cache_interface import CacheInterface


class MemRepoCache(CacheInterface):
    """Class for Cache in memory repository"""

    def __init__(self) -> None:
        self.cache = None

    def _set_cache_regras_ia(self, cache: list[dict]):
        self.cache = json.dumps(cache)

    def _obter_regras(self, filters: dict = None):
        result = [Regra.from_dict(r) for r in json.loads(self.cache)]

        if filters is None:
            return result

        if 'regra_id__eq' in filters:
            result = [
                r for r in result if r.regra_id == filters['regra_id__eq']
            ]

        if 'regra_id__in' in filters:
            result = [
                r for r in result if r.regra_id in filters['regra_id__in']
            ]

        if 'antecedentes_ids__eq' in filters:
            result = [
                r
                for r in result
                if set(r.antecedentes) == set(filters['antecedentes_ids__eq'])
            ]

        if 'consequentes_ids__eq' in filters:
            result = [
                r
                for r in result
                if set(r.consequentes) == set(filters['consequentes_ids__eq'])
            ]

        return result

    def _obter_regras_por_antecedentes(
        self, categoria_ids: list[int]
    ) -> list[int]:
        return [
            r['regra_id']
            for r in json.loads(self.cache)
            if set(r['antecedentes']) == set(categoria_ids)
        ]

    def _obter_consequentes_por_regra(self, regra_ids: list[int]):
        consequentes = []
        list_of_consequentes_list = [
            r['consequentes']
            for r in json.loads(self.cache)
            if r['regra_id'] in regra_ids
        ]
        for c in list_of_consequentes_list:
            consequentes.extend(c)
        return list(set(consequentes))
