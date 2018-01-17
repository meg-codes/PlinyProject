from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from prosopography.forms import SearchForm
from prosopography.models import Person, SocialField

Y = SocialField.DEFINITE
N = SocialField.NOT


class TestPersonListView(TestCase):

    def setUp(self):
        self.route = reverse('people:search')
        self.quintus = Person.objects.create(
            nomina='Quintus', equestrian=Y
        )
        self.gaius = Person.objects.create(
            nomina='Gaius',
            equestrian=N,
            senatorial=N,
            citizen=Y
        )
        self.senator = Person.objects.create(
            nomina='Senator',
            senatorial=Y,
            equestrian=N,
            citizen=Y
        )

    def test_get_context_data(self):

        res = self.client.get(self.route, {'foo': 'bar', 'page': '1'})
        context = res.context
        assert isinstance(context['form'], SearchForm)
        assert context['saved_query'] == '&foo=bar'

    def test_get_queryset(self):
        # no query string at all
        res = self.client.get(self.route)
        context = res.context
        # all objects in query list
        assert 'object_list' in context
        assert len(context['object_list']) == 3
        # search for Gaius
        res = self.client.get(self.route, {'nomina': 'Gai'})
        context = res.context
        assert 'object_list' in context
        assert len(context['object_list']) == 1
        assert context['object_list'][0] == self.gaius
        # search for senatorial class
        res = self.client.get(self.route, {'senatorial': 'Y'})
        context = res.context
        assert 'object_list' in context
        assert len(context['object_list']) == 1
        assert context['object_list'][0] == self.senator
        # search for equestrian
        res = self.client.get(self.route, {'equestrian': 'Y'})
        context = res.context
        assert 'object_list' in context
        assert len(context['object_list']) == 1
        assert context['object_list'][0] == self.quintus
        # search for citizen only
        res = self.client.get(self.route, {'citizen': 'Y'})
        context = res.context
        assert 'object_list' in context
        assert len(context['object_list']) == 1
        assert context['object_list'][0] == self.gaius
        # compound search citizen only and equestrian
        res = self.client.get(self.route, {'citizen': 'Y', 'equestrian': 'Y'})
        context = res.context
        assert 'object_list' in context
        assert len(context['object_list']) == 2
        assert self.gaius in context['object_list']
        assert self.quintus in context['object_list']




class PersonAutoCompleteDAL(TestCase):

    def setUp(self):

        self.quintus = Person.objects.create(nomina='Quintus')
        self.gaius = Person.objects.create(nomina='Gaius')

        self.user = get_user_model().objects.create_user(
            username='foo',
            password='bar'
        )
        self.user.is_staff = True
        self.user.save()

    def test_get(self):
        auto = reverse('people:dal-autocomplete')
        # no query string, no login, 302
        res = self.client.get(auto)
        assert res.status_code == 302

        # logged in, should get both created people
        self.client.login(username='foo', password='bar')
        res = self.client.get(auto)
        data = res.json()
        assert data
        assert 'results' in data
        assert len(data['results']) == 2

        # search for Qu
        res = self.client.get(auto, {'q': 'Qu'})
        assert res.status_code == 200
        data = res.json()
        assert len(data['results']) == 1
        # should get back Quintus' nomina
        print(data['results'])
        assert data['results'][0]['text'] == 'Quintus'


class PersonAutocomplete(TestCase):

    def setUp(self):

        self.quintus = Person.objects.create(nomina='Quintus')
        self.gaius = Person.objects.create(nomina='Gaius')

    def test_get(self):
        auto = reverse('people:autocomplete')
        # no query string
        res = self.client.get(auto)
        assert res.status_code == 200
        data = res.json()
        assert not data
        # search for Qu
        res = self.client.get(auto, {'q': 'Qu'})
        assert res.status_code == 200
        data = res.json()
        # should get back Quintus' nomina
        assert data[0] == 'Quintus'
