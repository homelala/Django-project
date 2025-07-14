from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.category import CategoryViewSet
from api.views.comment import CommentViewSet
from api.views.post import PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("categories", CategoryViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
