import redis
from django.db import transaction
from django.db.models import F

from api.errors import RedisLockConflictException
from api.model.models import Post
import logging
logger = logging.getLogger(__name__)

class PostService:
    @classmethod
    def like_with_f_transaction(cls, pk):
        # F 원자적 연산 사용 -> 매우 짧은 시간에만 락이 걸려 다른 요청들에 대해서는 문제가 되지 않음
        Post.objects.filter(pk=pk).update(like=F('like') + 1)
        return Post.objects.get(pk=pk)

    @classmethod
    def like_with_db_transaction(cls, pk):
        # sqlite는 행단위 락이 지원되지 않음 그러므로 테이블 락이 발생하는데 다른 요청들은 락으로 인해 대기하지 못하고 에러를 반환
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=pk)
            post.like += 1
            post.save()

        return post

    @classmethod
    def like_with_redis_lock(cls, pk):
        lock_key = f"lock:post:like:{pk}"
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        LOCK_EXPIRE = 1

        # Redis에 락 획득 시도 (setnx 방식)
        have_lock = redis_client.set(lock_key, "locked", nx=True, ex=LOCK_EXPIRE)

        if not have_lock:
            logger.warning(f"[RedisLock] 중복 요청: post_id={pk}")
            raise RedisLockConflictException("이미 처리 중입니다.", 429)
        try:
            # DB 원자적 처리
            Post.objects.filter(pk=pk).update(like=F('like') + 1)
            post = Post.objects.get(pk=pk)
        finally:
            # 락 해제
            redis_client.delete(lock_key)

        return post