from django.test import TestCase
from django.urls import reverse

from prosopography.models import Person


class TestPersonAutocomplete(TestCase):

    def setUp(self):

        self.quintus = Person.objects.create(nomina='Quintus')
        self.gaius = Person.objects.create(nomina='Gaius')

    def test_get(self):
        auto = reverse('people:autocomplete')
        # no query string, no result
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
