from src.drivers.implicit_recommender import SparseMatrixBuilder
from src.recomendacao.concrete_strategy_implicit import (
    ConcreteStrategyImplicit,
)
from src.recomendacao.implicit_recommender import ImplicitRecommender
from src.recomendacao.training_pipeline import TrainingPipeline
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo


def composer_pipeline_implicit(
    *, algorithm: str, client_id: int, params: dict
):

    strategy = ConcreteStrategyImplicit(
        algorithm=ImplicitRecommender(
            params=params, matrix_builder=SparseMatrixBuilder()
        ),
        repo_cache=RedisRepository(),
        repo_db=BasePostgresRepo(),
        client_id=client_id,
        params=params,
    )

    pipeline = TrainingPipeline(
        strategy=strategy,
        algorithm=algorithm,
        repo_db=BasePostgresRepo(),
        client_id=client_id,
        params=params,
    )

    pipeline.execute()
