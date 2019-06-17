from rest_framework import serializers
from rest_framework.reverse import reverse

from news.models import Post 
from prosopography.models import Person


class MultiKwargHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):

    lookup_fields = [('pk', 'pk')]

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', self.lookup_fields)
        super().__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):

        kwargs = {}
        for field, kwarg in self.lookup_fields:
            kwargs[kwarg] = getattr(obj, field, None)
        return reverse(view_name, kwargs=kwargs, request=request,
                       format=format)


class PersonListSerializer(serializers.ModelSerializer):

    url = MultiKwargHyperlinkedIdentityField(
        view_name='prosopography:detail', 
        lookup_fields=[
            ('pk', 'id'),
            ('slug', 'slug')
        ])
    letters_to = serializers.StringRelatedField(many=True)

    class Meta:
        model = Person
        fields = ('pk', 'url', 'nomina', 'ordo', 'letters_to')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')