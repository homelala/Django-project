from rest_framework import viewsets

from api.model.models import Comment
from api.serilalizers.comment import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



