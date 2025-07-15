from contextlib import contextmanager
from redlock import RedLockFactory

from api.errors import RedisLockConflictException
import logging
logger = logging.getLogger(__name__)

factory = RedLockFactory(
    connection_details=[
        {"host": "localhost", "port": 6379, "db": 0},
        {"host": "localhost", "port": 6380, "db": 0},
        {"host": "localhost", "port": 6381, "db": 0},
    ]
)


@contextmanager
def create_lock(resource_key, ttl=5000):
    """
    분산 락 생성 및 해제
    :param resource_key: 락을 걸 Redis 키
    :param ttl: 락 유지 시간 (ms 단위)
    """
    lock = factory.create_lock(
        resource_key,
        ttl=ttl,
        retry_times=2,  # 락 재시도 횟수
        retry_delay=200,
    )

    if not lock.acquire():
        logger.warning(f"[LOCK-FAIL] 락 획득 실패: {resource_key}")
        raise RedisLockConflictException(f"[LOCK] Unable to acquire lock for key: {resource_key}", 429)

    try:
        logger.info(f"락 획득 성공: {resource_key}")
        yield
    finally:
        try:
            lock.release()
            logger.info(f"락 해제 완료: {resource_key}")
        except Exception as e:
            logger.warning(f"락 해제 실패: {resource_key} - {str(e)}")

def create_post_redlock(post_id):
    return create_lock(RedLockKey.get_post_key(post_id))


class RedLockKey:
    @classmethod
    def get_post_key(cls, post_id):
        return f"Post:{post_id}"
