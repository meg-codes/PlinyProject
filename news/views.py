import hashlib

from django.views.generic import ListView
from prosopography.forms import SearchForm
from .models import Post


class PostListView(ListView):

    model = Post
    paginate_by = 3
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):

        context = super(PostListView, self).get_context_data()
        context['form'] = SearchForm()
        return context
