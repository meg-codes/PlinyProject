from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .views import PostListView
from .models import Post


class TestPost(TestCase):

    def test_str(self):
        post = Post.objects.create(subject='foo', content='bar')
        assert isinstance(post, Post)
        print(str(post))
        assert str(post) == "%s - foo" % timezone.now().date()


class TestPostListView(TestCase):

    def setUp(self):
        Post.objects.create(subject='foo', content='bar')
        post2 = Post.objects.create(subject='baz', content='foo')
        post2.date_posted = timezone.now() - timedelta(days=2)

    def test_view(self):
        view_url = reverse('index')
        response = self.client.get(view_url)
        used_templates = ['news/post_list.html', 'pp_base.html',
                          'footer.html', 'top_nav.html',
                          'django/forms/widgets/text.html',
                          'django/forms/widgets/input.html',
                          'django/forms/widgets/attrs.html', ]

        assert response.status_code == 200
        for template in response.templates:
            assert template.name in used_templates
        assert 'paginator' in response.context
        page = response.context['paginator'].page(1)
        assert page
        assert not page.has_next()
        assert not page.has_previous()
        for i in range(1, 3):
            Post.objects.create(subject='foo', content='bar')

        response = self.client.get(view_url)
        assert 'paginator' in response.context
        assert response.context['paginator'].page_range == range(1, 3)
