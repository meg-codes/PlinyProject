from django.views.generic import ListView
from .models import Post


class PostListView(ListView):

    model = Post
    paginate_by = 10
    context_object_name = 'posts'
