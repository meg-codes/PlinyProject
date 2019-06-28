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


class ChicagoCitationField(serializers.RelatedField):

    def to_representation(self, value):
        return value.chicago


class PersonDetailSerializer(serializers.ModelSerializer):

    letters_to = serializers.StringRelatedField(many=True)
    citations = ChicagoCitationField(many=True, read_only=True)
    gender = serializers.CharField(source="get_gender_display")
    citizen = serializers.CharField(source="get_citizen_display")
    equestrian = serializers.CharField(source='get_equestrian_display')
    senatorial = serializers.CharField(source='get_senatorial_display')
    consular = serializers.CharField(source='get_consular_display')

    class Meta:
        model = Person
        fields = ('__all__')


class PersonAutocomplete(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'nomina')

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