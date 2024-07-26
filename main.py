import concurrent.futures
import logging
import time

from src.drivers import scheduler
from src.main.composers.pipeline_compose_implicit import (
    composer_pipeline_implicit,
)
from src.main.composers.pipeline_composer_apriori import (
    composer_pipeline_apriori,
)
from src.repository.cache.redisrepo_regra import RedisRepository
from src.repository.model_manager import ModelManager
from src.repository.postgres.base_postgresrepo import BasePostgresRepo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize ModelManager during application startup for pre-loading models
global_model_manager = ModelManager(
    repo_db=BasePostgresRepo(), repo_cache=RedisRepository()
)
global_model_manager.load_models_from_cache()


def run_composer(client_id, algorithm, parameters_dict, composer_pipelines):
    try:
        logger.info(f'Running pipeline-{algorithm} for client ID {client_id}')

        if algorithm not in composer_pipelines:
            raise ValueError(f'Algorithm not listed "{algorithm}"')

        composer_func = composer_pipelines[algorithm]
        logger.debug(f'Composer function: {composer_func.__name__}')
        composer_func(
            algorithm=algorithm, client_id=client_id, params=parameters_dict
        )
        logger.debug(
            f'Composer function {composer_func.__name__} executed successfully'
        )

    except Exception as e:
        logger.error(f'Error in pipeline for client ID {client_id}: {e}')


def main():

    COMPOSER_PIPELINES = {
        'apriori': composer_pipeline_apriori,
        'implicit': composer_pipeline_implicit,
    }

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                run_composer,
                client_id,
                algorithm,
                parameters_dict,
                COMPOSER_PIPELINES,
            )
            for client_id, algorithm, parameters_dict in global_model_manager.generate_rows()
        ]

        concurrent.futures.wait(futures)

    global_model_manager.load_models_from_cache()


if __name__ == '__main__':
    scheduler.add_job(main, minutes=1)
    scheduler.start_job()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Encerrar o agendador de forma adequada ao receber um sinal de interrupção
        scheduler.shutdown()
