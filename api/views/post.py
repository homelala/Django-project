from django.db import transaction
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.model.models import Post
from api.serilalizers.serializers import PostSerializer, PostDetailSerializer, PostPrevNextSerializer, \
    CommentListSerializer, PostFilter
from api.service.post import PostService
from api.utils import prev_next_post

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        instance = Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set').get(pk=pk)
        prev_dict, next_dict = prev_next_post(instance)
        comment_list = instance.comment_set.all()

        dataDict = {
            "post": PostDetailSerializer(instance).data,
            "prevPost": PostPrevNextSerializer(prev_dict).data if prev_dict else None,
            "nextPost": PostPrevNextSerializer(next_dict).data if next_dict else None,
            "commentList": CommentListSerializer(comment_list, many=True).data,
        }

        return Response(dataDict)

    @action(detail=True, methods=["patch"])
    def like(self, request, pk=None):
        # post = self.get_object()
        # post.increase_like()
        # post.save()

        # post = PostService.like_with_f_transaction(pk)
        post = PostService.like_with_db_transaction(pk)

        return Response({"like": post.like}, status=status.HTTP_200_OK)

