from django.test import TestCase
from django.utils import timezone
from .models import Post


class TestPost(TestCase):

    def test_str(self):
        post = Post.objects.create(subject='foo', content='bar')
        assert isinstance(post, Post)
        assert str(timezone.now().date()) in str(post)
        assert " - foo" in str(post)
