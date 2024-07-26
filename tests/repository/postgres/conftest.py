"""Configuratin module for integration testing for Postgres
The fixtures contains code that is specific to Postgres, so it is better to
keep the code separated in a more specific file conftest.py
"""

# pylint: disable=w0621
# pylint: disable=c0116
# pylint: disable=c0103
# pylint: disable=c0209
import pytest
import sqlmodel

from src.repository.postgres.postgres_objects import Product as PgProduct


@pytest.fixture(scope='session')
def pg_session_empty(app_configuration):
    conn_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        app_configuration['POSTGRES_USER'],
        app_configuration['POSTGRES_PASSWORD'],
        app_configuration['POSTGRES_HOSTNAME'],
        app_configuration['POSTGRES_PORT'],
        app_configuration['APPLICATION_DB'],
    )

    engine = sqlmodel.create_engine(conn_str)
    connection = engine.connect()

    sqlmodel.SQLModel.metadata.create_all(engine)
    sqlmodel.SQLModel.metadata.bind = engine

    DBSession = sqlmodel.Session(bind=engine)
    session = DBSession

    yield session

    session.close()
    connection.close()


@pytest.fixture(scope='session')
def pg_product_test_data():
    return [
        {
            'nome': 'Produto A',
            'descricao': 'descricao A',
            'sku': '0123456789',
            'categoria_id': 1,
            'ativo': True,
        },
        {
            'nome': 'Produto B',
            'descricao': 'descricao B',
            'sku': '0123456789',
            'categoria_id': 1,
            'ativo': True,
        },
        {
            'nome': 'Produto C',
            'descricao': 'descricao C',
            'sku': '0123456789',
            'categoria_id': 2,
            'ativo': False,
        },
        {
            'nome': 'Produto D',
            'descricao': 'descricao D',
            'sku': '0123456789',
            'categoria_id': 2,
            'ativo': False,
        },
    ]


@pytest.fixture(scope='package')
def pg_session(
    pg_session_empty,
    pg_product_test_data,
):
    """Fills the database with Postgress objects created with the test data for
    every test that is run. These are not entities, but Postgress objects we
    create to map them.
    """
    for product in pg_product_test_data:
        # Assuming the FK relationship between category and product
        new_product = PgProduct(**product)

        pg_session_empty.add(new_product)
        pg_session_empty.commit()

    yield pg_session_empty

    # Clean up after test
    pg_session_empty.query(PgProduct).delete()
