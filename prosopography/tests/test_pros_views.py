from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from prosopography.models import Person


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
