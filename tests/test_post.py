from threading import Thread

import pytest

from tests.factories.post import PostFactory
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


class Describe_PostViewSet:
    @pytest.fixture()
    def post(self):
        return PostFactory.create()

    class Context_retrieve:
        @pytest.mark.django_db
        def test_post_retrieve(self, api_client, post):
            url = reverse("post-detail", kwargs={"pk": post.pk})
            response = api_client.get(url)

            assert response.status_code == 200
            assert response.data["post"]["title"] == post.title
            assert response.data["post"]["content"] == post.content

    class Test_like:
        @pytest.mark.django_db
        def test_post_like(self, api_client, post):
            url = reverse("post-like", kwargs={"pk": post.pk})
            old_like = post.like

            response = api_client.patch(url)

            post.refresh_from_db()
            assert response.status_code == 200
            assert post.like == old_like + 1
            assert response.data["like"] == post.like

        @pytest.mark.django_db(transaction=True)
        def test_post_like_concurrent(self, api_client, post):
            url = reverse("post-like", kwargs={"pk": post.pk})
            thread_count = 10
            responses = []

            def send_like():
                response = api_client.patch(url)
                responses.append(response)

            threads = [Thread(target=send_like) for _ in range(thread_count)]

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            old_like = post.like
            post.refresh_from_db()

            # 성공한 요청 수 확인
            success_responses = [r for r in responses if r.status_code == 200]
            rejected_responses = [r for r in responses if r.status_code == 429]

            assert post.like == old_like + len(success_responses)
            assert len(success_responses) + len(rejected_responses) == thread_count
