from rest_framework import viewsets

from api.model.models import Category
from api.serilalizers.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer