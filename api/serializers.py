from rest_framework import serializers
from rest_framework.reverse import reverse

from news.models import Post
from prosopography.models import Person


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
        fields = ('nomina',)


class PersonListSerializer(serializers.ModelSerializer):

    url = serializers.URLField(source='get_absolute_url') 
    letters_to = serializers.StringRelatedField(many=True)

    class Meta:
        model = Person
        fields = ('pk', 'url', 'nomina', 'ordo', 'letters_to')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')