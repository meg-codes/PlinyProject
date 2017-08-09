import hashlib

from django.views.decorators.http import condition
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from prosopography.forms import SearchForm
from .models import Post


def last_mod(request):
    return Post.objects.latest('date_updated').date_updated


@method_decorator(condition(last_modified_func=last_mod), name='dispatch')
class PostListView(ListView):

    model = Post
    paginate_by = 3
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):

        context = super(PostListView, self).get_context_data()
        context['form'] = SearchForm()
        return context
