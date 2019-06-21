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
            cumulative_query = None
            if 'citizen' in social_class:
                cumulative_query = Q(citizen='Y') & Q(equestrian='N') \
                    & Q(senatorial='N')
            if 'equestrian' in social_class:
                equestrian = Q(equestrian='Y')
                if cumulative_query is None:
                    cumulative_query = equestrian
                else:
                    cumulative_query |= equestrian
            if 'senatorial' in social_class:
                senatorial = Q(senatorial='Y')
                if cumulative_query is None:
                    cumulative_query = senatorial
                else:
                    cumulative_query |= senatorial
            queryset = queryset.filter(cumulative_query)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostListView(generics.ListAPIView):
    serializer_class = api_serializers.PostSerializer
    queryset = Post.objects.all()
