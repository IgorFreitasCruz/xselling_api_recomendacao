class MemRepoRecomendacao:
    """Class for Recomendacao in memory repository"""

    def __init__(self, data: list[dict]) -> None:
        self.data = data

    def _obter_categoria_by_produto(
        self, *, produto_sku: list[str]
    ) -> list[int]:
        return [
            p['categoria_id'] for p in self.data if p['sku'] in produto_sku
        ]

    def _obter_produto_recomendado(
        self, *, consequente_ids: list[int]
    ) -> list[int]:
        return [
            {
                'nome': p['nome'],
                'descricao': p['descricao'],
                'categoria_id': p['categoria_id'],
                'sku': p['sku'],
            }
            for p in self.data
            if p['categoria_id'] in consequente_ids
        ]
