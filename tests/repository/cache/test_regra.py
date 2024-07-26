import pytest

from src.errors.types.http_exception_redis import RedisExceptionError
from src.repository.cache.redisrepo_regra import RedisRepository

# The module attribute pytestmark labels every test in the module with the tag integration
pytestmark = pytest.mark.integration


def test_fetch_all_values():
    # Arrange

    redis_repo = RedisRepository()
    key = 'test_key'
    value1 = 'value1'

    redis_repo.set_all(key, value1)

    # Act
    result = redis_repo.get_all(key)

    # Assert
    assert result == [value1]


def test_set_new_key_value_pair():
    # Arrange
    redis_repo = RedisRepository()
    key = 'test_key'
    value = 'test_value'

    # Act
    result = redis_repo.set_all(key, value)

    # Assert
    assert result == {'message': 'Data set successfully'}
    assert redis_repo.get_all(key) == [value]


def test_handle_empty_keys():
    # Arrange
    redis_repo = RedisRepository()

    # Act
    result = redis_repo.get_all('nonexistent_key')

    # Assert
    assert result == []


def test_handle_get_all_error(mocker):
    # Arrange
    redis_repo = mocker.Mock()
    redis_repo.get_all.side_effect = RedisExceptionError('Some error message')

    # Act and Assert
    with pytest.raises(RedisExceptionError):
        redis_repo.get_all('some_value')


def test_handle_set_all_error(mocker):
    # Arrange
    redis_repo = mocker.Mock()
    redis_repo.set_all.side_effect = RedisExceptionError('Some error message')
    key = 'test_key'
    value = 'test_value'

    # Act and Assert
    with pytest.raises(RedisExceptionError):
        redis_repo.set_all(key, value)
