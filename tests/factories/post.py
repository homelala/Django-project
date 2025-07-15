import factory
from factory.django import DjangoModelFactory

from api.model.models import Post, Category


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f"Post {n}")
    content = "Sample content"
    category = factory.SubFactory(CategoryFactory)
    like = 0
