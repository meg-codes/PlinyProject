from rest_framework import generics, mixins, pagination
from django.db.models import Q


import api.serializers as api_serializers
from news.models import Post
from prosopography.models import Person


class TwentyPagesPagination(pagination.PageNumberPagination):
    page_size = 20


class PersonListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = api_serializers.PersonListSerializer
    pagination_class = TwentyPagesPagination

    def get_queryset(self):

        queryset = Person.objects.all()
        nomina = self.request.query_params.get('nomina', None)
        if nomina:
            queryset = queryset.filter(nomina__icontains=nomina)

        social_class = self.request.query_params.getlist('socialClass', None)
        if social_class:
            q_object = None
            for ordo in social_class:
                if q_object is None:
                    q_object = Q(**{ordo: 'Y'})
                else:
                    q_object |= Q(**{ordo: 'Y'})
            queryset = queryset.filter(q_object)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostListView(generics.ListAPIView):
    serializer_class = api_serializers.PostSerializer
    queryset = Post.objects.all()
