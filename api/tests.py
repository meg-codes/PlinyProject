from unittest.mock import Mock

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from api.serializers import ChicagoCitationField
from news.models import Post


class TestChicagoSerializer(SimpleTestCase):

    def test_to_representation(self):
        chicago_field = ChicagoCitationField(read_only=True)
        mock_person = Mock()
        mock_person.chicago = "Fake Citation"
        output = chicago_field.to_representation(mock_person)
        assert output == "Fake Citation"


class TestPersonListView(TestCase):

    fixtures = ['people_fixture.json']

    def test_get(self):
        # all three results are returned
        url = reverse('api:people')
        res = self.client.get(url)
        output = res.json()
        assert 'results' in output
        assert len(output['results']) == 3
        # filter by nomina
        res = self.client.get(url, {'nomina': 'tac'})
        output = res.json()
        assert len(output['results']) == 1
        assert output['results'][0]['nomina'] == 'Cornelius Tacitus'
        # filter by social class
        res = self.client.get(url, {'socialClass': 'citizen'})
        output = res.json()
        assert len(output['results']) == 0
        res = self.client.get(url, {'socialClass': 'senatorial'})
        output = res.json()
        assert len(output['results']) == 2
        res = self.client.get(url, {'socialClass': 'equestrian'})
        output = res.json()
        assert len(output['results']) == 1


class TestPersonAutocompleteView(TestCase):

    fixtures = ['people_fixture']
    
    def test_get(self):
        res = self.client.get(reverse('api:autocomplete'))
        assert res.json() == [
            {'nomina': 'Cornelius Tacitus'}, 
            {'nomina': 'L. Calpurnius Fabatus'}, 
            {'nomina': 'Novius Maximus'}
        ]


class TestPersonDetailView(TestCase):

    fixtures = ['people_fixture']

    def test_get(self):
        res = self.client.get(reverse('api:person-detail', args=[1]))
        assert res.json() == {
            'id': 1, 
            'letters_to': [], 
            'citations': [],
            'gender': 'Male',
            'citizen': 'Yes', 
            'equestrian': 'No', 
            'senatorial': 'Yes', 
            'consular': 'Yes', 
            'nomina': 'Cornelius Tacitus', 
            'birth': None, 
            'death': None, 
            'cos': None, 
            'cos_suff': 97, 
            'floruit': None, 
            'certainty_of_id': 5, 
            'notes': '', 
            'from_comum': False, 
            'mentioned_in': [], 
            'related_to': []
        }


class TestPostListView(TestCase):
    
    def test_get(self):

        Post.objects.create(
            subject='test1',
            content='test content 1'
        )
        Post.objects.create(
            subject='foo',
            content='bar'
        )

        res = self.client.get(reverse('api:posts'))
        output = res.json()
        assert len(output) == 2
        assert output[0]['subject'] == 'foo'
        assert output[1]['subject'] == 'test1'

