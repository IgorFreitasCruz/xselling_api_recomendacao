from src.recomendacao.apriori_recommender import AprioriRecommender
from src.recomendacao.concrete_strategy_apriori import ConcreteStrategyApriori
from src.recomendacao.training_pipeline import TrainingPipeline
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.postgres.base_postgresrepo import BasePostgresRepo


def composer_pipeline_apriori(*, algorithm: str, client_id: int, params: dict):

    strategy = ConcreteStrategyApriori(
        algorithm=AprioriRecommender(**params),
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
