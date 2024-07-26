from src.domain.regra import Regra
from src.errors.types import NotFoundError
from src.repository.in_memory.memrepo_cache import MemRepoCache


class RegraListUseCase:
    def __init__(self, regra_repository: MemRepoCache) -> None:
        self.regra_repository = regra_repository

    def execute(self, *, request: dict) -> dict:
        categorias: list[int] = self.__format_request(request)
        regras: list[Regra] = self.__search_regra(categoria_ids=categorias)
        response: dict = self.__format_response(regras=regras)
        return response

    @staticmethod
    def __format_request(request) -> list[int]:
        """Formatação do payload de entrada

        Args:
            request (dict): objeto do request adapter

        Returns:
            list[int]: Lista com ids das categorias
        """
        produtos = request['produtos']
        categorias: list[int] = [
            p['categoria_id']
            for p in produtos
            if p['categoria_id'] is not None
        ]
        return categorias

    def __search_regra(self, categoria_ids: list[int]) -> list[Regra]:
        """Busca de regras através das categorias dos produtos

        Args:
            categoria_ids (list[int): Lista com ids das categorias

        Raises:
            NotFoundError: "Regra não encontrada"

        Returns:
            list[Regra]: Lista de entidades de Regra
        """
        regras = self.regra_repository._obter_regras_por_antecedentes(
            categoria_ids=categoria_ids
        )
        if regras == []:
            raise NotFoundError('Regra não encontrada')
        return regras

    @staticmethod
    def __format_response(regras: list[Regra]) -> dict:
        """Formatação do payload de resposta

        Args:
            regras (list[Regra]): Lista de dicionários de entidades de Regra

        Returns:
            dict: Dicionário formatado com regras selecionadas
        """
        result = {'type': 'Regra', 'count': len(regras), 'attributes': regras}
        return result
