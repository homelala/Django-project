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
        from api.infra.redis import create_post_redlock

        with create_post_redlock(pk):
            Post.objects.filter(pk=pk).update(like=F('like') + 1)
            post = Post.objects.get(pk=pk)
        return post