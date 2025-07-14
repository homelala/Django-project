from rest_framework import serializers

from api.model.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["created_at", "updated_at"]