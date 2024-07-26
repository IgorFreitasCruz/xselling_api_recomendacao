import csv
import json
from unittest import mock

import pandas as pd
import pytest

from src.main.composers.pipeline_compose_implicit import (
    composer_pipeline_implicit,
)
from src.main.composers.pipeline_composer_apriori import (
    composer_pipeline_apriori,
)
from src.recomendacao.apriori_recommender import AprioriRecommender
from src.recomendacao.implicit_recommender import ImplicitRecommender
from src.recomendacao.training_pipeline import TrainingPipeline
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo


@pytest.fixture
def training_dataset():
    return pd.read_csv(
        'tests/drivers/recomendacao.csv',
        sep=',',
        header=1,
        names=['num_pedido', 'categorias'],
    )


@pytest.fixture
def lista_produtos():
    with open('tests/drivers/lista_produtos.csv') as f:
        csv_reader = csv.reader(f)
        return list(csv_reader)


@pytest.fixture
def regras_df_bruto():
    return pd.read_pickle(
        'tests/drivers/regras.pkl',
    )


def test_busca_dados_no_storage(training_dataset):
    recomendacao = mock.Mock(spec=TrainingPipeline)
    recomendacao.busca_dados_no_storage.return_value = training_dataset

    result = recomendacao.busca_dados_no_storage()

    assert isinstance(result, pd.DataFrame)


def test_formata_dataframe_treinamento(training_dataset):
    params = {
        'min_support': 0.2,
        'min_threshold': 0.5,
        'metric': 'confidence',
    }

    recomendacao = TrainingPipeline(
        recomendacao_algoritmo=AprioriRecommender(
            min_support=params['min_support'],
            min_threshold=params['min_threshold'],
            metric=params['metric'],
        ),
        repo_cache=RedisRepository(),
        repo_db=BasePostgresRepo(),
        client_id=1,
        params=params,
        cnpj='00.000.000/0000-01',
    )
    result = recomendacao._TrainingPipeline__formata_dataframe_treinamento(
        training_dataset
    )
    print(result)

    assert isinstance(result, list)


def test_AprioriRecommender__cria_matriz_incidencia(lista_produtos):
    algoritmo_recomendacao = AprioriRecommender(
        produtos_list=lista_produtos,
        min_support=0.0025,
        min_threshold=0.35,
        metric='confidence',
    )

    result = (
        algoritmo_recomendacao._AprioriRecommender__cria_matriz_incidencia(
            lista_produtos
        )
    )

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] > 0


def test_AprioriRecommender__cria_conjuntos_de_produtos(lista_produtos):
    algoritmo_recomendacao = AprioriRecommender(
        produtos_list=lista_produtos,
        min_support=0.0025,
        min_threshold=0.35,
        metric='confidence',
    )

    matrix_incidencia = (
        algoritmo_recomendacao._AprioriRecommender__cria_matriz_incidencia(
            lista_produtos
        )
    )
    result = (
        algoritmo_recomendacao._AprioriRecommender__cria_conjuntos_de_produtos(
            matrix_incidencia
        )
    )

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] > 0


def test_AprioriRecommender(lista_produtos):
    algoritmo_recomendacao = AprioriRecommender(
        min_support=0.0025,
        min_threshold=0.35,
        metric='confidence',
    )

    algoritmo_recomendacao.set_parameters(lista_produtos)

    result = algoritmo_recomendacao.execute()

    # result.to_pickle('tests/drivers/regras.pkl')

    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] > 0


def test_formata_dataframe_output_treinamento(regras_df_bruto):
    recomendacao = TrainingPipeline()
    print()
    # print(regras_df_bruto)
    (
        regras_associacao,
        regras_antecedentes,
        regras_consequentes,
    ) = recomendacao.formata_dataframe_output_treinamento(regras_df_bruto)
    # response = recomendacao.salva_output_treinamento_no_banco(regras_associacao)

    # print()
    # print(regras_associacao)
    # print()
    # print(regras_antecedentes)
    # print()
    # print(regras_consequentes)

    # assert set(result.columns) == set(['descricao_regra', 'confianca', 'suporte', 'lift', 'dt_inclusao', 'ativo'])
    # assert response > 0


def test_load_data_to_cache(regras_df_bruto):
    recomendacao = TrainingPipeline(cache_repo=RedisRepository)

    result = recomendacao.salva_output_treinamento_no_cache()


def test_query_dados_treino():
    repo = TrainingPipeline(
        repo_cache=RedisRepository(),
        repo_db=BasePostgresRepo(),
        recomendacao_algoritmo=AprioriRecommender(
            min_support=0.02,
            min_threshold=0.5,
            metric='confidence',
        ),
        cnpj='00.000.000/0000-01',
        client_id=1,
        params={
            'min_support': 0.02,
            'min_threshold': 0.5,
            'metric': 'confidence',
        },
    )

    # dados_para_treino = repo.busca_dados_no_storage()
    # dados_para_treino_formatados = repo.formata_dataframe_treinamento(
    #     dados_para_treino
    # )
    # regras_associacao = repo.executa_algoritmo_de_recomendacao(
    #     produtos_list=dados_para_treino_formatados
    # )
    # (
    #     regras_associacao,
    #     regras_antecedentes,
    #     regras_consequentes,
    # ) = repo.formata_dataframe_output_treinamento(
    #     regras_associacao=regras_associacao
    # )

    # result = repo.salva_output_treinamento_no_banco(
    #     regras_associacao=regras_associacao,
    #     regras_antecedentes_temp=regras_antecedentes,
    #     regras_consequentes_temp=regras_consequentes,
    # )
    repo._TrainingPipeline__salva_output_treinamento_no_cache()


def test_pipeline_completo():
    clientes = [
        {
            'client_id': 1,
            'algoritmo': 'apriori',
            'params': {
                'min_support': 0.01,
                'min_threshold': 0.5,
                'metric': 'confidence',
            },
        },
    ]

    for cliente in clientes:
        import sys

        print(
            '*' * 20,
            __name__,
            ': line',
            sys._getframe().f_lineno,
            '*' * 20,
            flush=True,
        )
        print(cliente['client_id'], flush=True)
        composer_pipeline_apriori(
            algorithm=cliente['algoritmo'],
            client_id=cliente['client_id'],
            params=cliente['params'],
        )


def test_pipeline_completo_implicit():
    clientes = [
        {
            'client_id': 1,
            'algoritmo': 'implicit',
            'params': {'algo_type': 'als'},
        },
    ]

    for cliente in clientes:
        import sys

        print(
            '*' * 20,
            __name__,
            ': line',
            sys._getframe().f_lineno,
            '*' * 20,
            flush=True,
        )
        print(cliente['client_id'], flush=True)
        composer_pipeline_implicit(
            algorithm=cliente['algoritmo'],
            client_id=cliente['client_id'],
            params=cliente['params'],
        )


def test_main():
    from main import main

    main()


def test_load_data_to_cache1():
    repo = BasePostgresRepo()
    repo_cache = RedisRepository()
    query = """ SELECT
                    p.sku, c.id, c.descricao, p.nome
                FROM category c
                INNER JOIN product p
                ON c.id = p.categoria_id;"""

    with repo.engine.begin() as connection:
        result = connection.exec_driver_sql(query).fetchall()
        df = pd.DataFrame(result)
    sku_to_prod = (
        df.groupby('sku', group_keys=False)
        .apply(
            lambda group: group.drop('sku', axis=1).to_dict(orient='records')[
                0
            ]
        )
        .to_dict()
    )
    repo_cache.insert_hash(
        'cross_selling', 'sku_to_item', json.dumps(sku_to_prod)
    )


def test_load_data_to_cache2():
    repo = BasePostgresRepo()
    repo_cache = RedisRepository()
    query = """ SELECT
                c.id as id_categoria,
                p.nome,
                p.descricao as descricao_produto,
                c.descricao as descricao_categoria,
                p.sku,
                categoria_id
            FROM category c 
            INNER JOIN product p 
            ON c.id = p.categoria_id
            AND p.Ativo = 1;"""

    with repo.engine.begin() as connection:
        result = connection.exec_driver_sql(query).fetchall()
        df = pd.DataFrame(result)

    cat_id_to_prods = (
        df.groupby('id_categoria')
        .apply(
            lambda group: group.drop('id_categoria', axis=1).to_dict(
                orient='records'
            )
        )
        .to_dict()
    )
    repo_cache.insert_hash(
        'cross_selling', 'cat_id_to_items', json.dumps(cat_id_to_prods)
    )
