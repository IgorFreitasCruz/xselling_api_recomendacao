# pylint: disable=c0103
# pylint: disable=c0209
# pylint: disable=c0116
from src.domain import produto
from src.repository.postgres.base_postgresrepo import BasePostgresRepo
from src.repository.postgres.postgres_objects import Product as PgProduct


class PostgresRepoProduct(BasePostgresRepo):
    """Postgres Product repository"""

    def _create_product_objects(self, result: list[PgProduct]):
        return [
            produto.Product(
                id=p.id,
                code=p.code,
                nome=p.nome,
                descricao=p.descricao,
                sku=p.sku,
                categoria_id=p.categoria_id,
                dt_inclusao=p.dt_inclusao,
                dt_alteracao=p.dt_alteracao,
                ativo=p.ativo,
            )
            for p in result
        ]

    def list_product(self, filters=None) -> list[produto.Product]:
        session = self._create_session()

        query = session.query(PgProduct)

        if filters is not None:
            if 'id__eq' in filters:
                query = query.filter(PgProduct.id == filters['id__eq'])

            if 'code__eq' in filters:
                query = query.filter(PgProduct.code == filters['code__eq'])

            if 'ativo__eq' in filters:
                query = query.filter(PgProduct.ativo == filters['ativo__eq'])

            if 'categoria_id__eq' in filters:
                query = query.filter(
                    PgProduct.categoria_id == filters['categoria_id__eq']
                )

            if 'sku__eq' in filters:
                query = query.filter(PgProduct.sku == filters['sku__eq'])

        return self._create_product_objects(query.all())

    def _obter_categoria_by_produto(self, produto_sku: list) -> list[int]:
        with self.engine.begin() as connection:
            result = connection.exec_driver_sql(
                f"""SELECT c.id FROM category c
                INNER JOIN product p
                ON c.id = p.categoria_id
                WHERE p.sku in {tuple(produto_sku) if len(produto_sku) > 1 else (produto_sku[0], produto_sku[0])};"""
            ).fetchall()

            self.engine.dispose()

        # retornar os valores no formato de lista
        return [n[0] for n in result]

    def _obter_produto_recomendado(
        self, consequente_ids: list[int], produto_sku: list[str]
    ):
        with self.engine.begin() as connection:
            result = connection.exec_driver_sql(
                f"""SELECT
                        p.nome,
                        p.descricao,
                        p.sku,
                        c.descricao,
                        p.categoria_id
                    FROM
                        product p
                        INNER JOIN category c 
                            ON p.categoria_id = c.id 
                            AND p.ativo = 1
                    WHERE
                        c.id IN {tuple(consequente_ids) if len(consequente_ids) > 1 else (consequente_ids[0], consequente_ids[0])}
                        AND p.sku NOT IN {tuple(produto_sku) if len(produto_sku) > 1 else (produto_sku[0], produto_sku[0])};"""
            ).fetchall()

            self.engine.dispose()

        # Não alterar a ordem das Keys!
        keys = (
            'nome',
            'descricao',
            'sku',
            'categoria',
            'categoria_id',
        )

        return [dict(zip(keys, row)) for row in result]

    def fetch_item_by_sku(self, items_sku: list):
        with self.engine.begin() as connection:
            result = connection.exec_driver_sql(
                f"""SELECT nome
                        FROM product
                        where sku in {tuple(items_sku) if len(items_sku) > 1 else (items_sku[0], items_sku[0])};"""
            ).fetchall()

            self.engine.dispose()

        return [n[0] for n in result]
