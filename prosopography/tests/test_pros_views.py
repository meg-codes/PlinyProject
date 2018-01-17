from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from letters.models import Letter
from prosopography.forms import SearchForm
from prosopography.models import Person, SocialField
from prosopography.views import NodeEdgeListView, PersonDetailView

Y = SocialField.DEFINITE
N = SocialField.NOT


class TestPersonDetailView(TestCase):

    def setUp(self):
        self.quintus = Person.objects.create(
            nomina='Quintus', equestrian=Y
        )
        self.gaius = Person.objects.create(
            nomina='Gaius',
            equestrian=N,
            senatorial=N,
            citizen=Y
        )

    def test_get_object(self):
        detailview = PersonDetailView()
        detailview.kwargs = {}
        detailview.kwargs['id'] = self.gaius.pk
        detailview.kwargs['slug'] = 'quintus'
        obj = detailview.get_object()
        # should ignore slug and return gaius
        assert obj == self.gaius

    def test_render_to_response(self):
        # should return the object as expected if pk and slug match
        route = reverse('people:detail',
                        kwargs={'slug': 'gaius', 'id': self.gaius.pk})
        res = self.client.get(route)
        assert res.status_code == 200
        assert res.context['object'] == self.gaius
        # if they do not should return 302
        route = reverse('people:detail',
                        kwargs={'slug': 'quintus', 'id': self.gaius.pk})
        res = self.client.get(route)
        self.assertRedirects(res, self.gaius.get_absolute_url())


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


class TestNodeEdgeListView(TestCase):

    def setUp(self):
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
        self.consul = Person.objects.create(
            nomina='Consulis',
            senatorial=Y,
            consular=Y,
            citizen=Y
        )

        letter = Letter.objects.create(book=1, letter=2)
        self.gaius.letters_to.add(letter)
        self.quintus.letters_to.add(letter)
        self.consul.letters_to.add(letter)
        self.senator.letters_to.add(letter)
        self.senator.mentioned_in.add(letter)

    @patch('prosopography.views.NodeEdgeListView.get_data')
    def test_render_to_json_response(self, mockdata):
        mockdata.return_value = {}
        nodes = NodeEdgeListView()
        res = nodes.render_to_json_response()
        assert isinstance(res, JsonResponse)
        assert res.content == b'{}'

    def test_assign_class(self):
        nodes = NodeEdgeListView()
        assert nodes.assign_class(self.senator) == 3
        assert nodes.assign_class(self.gaius) == 1
        assert nodes.assign_class(self.quintus) == 2
        assert nodes.assign_class(self.consul) == 4

    def test_get_data(self):
        expected_dict = {
            'nodes': [
                {'id': 'Gaius Plinius Secundus', 'group': 9},
                {'id': 'Gaius', 'group': 1},
                {'id': 'Quintus', 'group': 2},
                {'id': 'Senator', 'group': 3},
                {'id': 'Consulis', 'group': 4},
            ],
            'links': [
                {'source': 'Gaius Plinius Secundus', 'target': 'Gaius', 'weight': 1},
                {'source': 'Gaius Plinius Secundus', 'target': 'Quintus', 'weight': 1},
                {'source': 'Gaius Plinius Secundus', 'target': 'Senator', 'weight': 2},
                {'source': 'Gaius Plinius Secundus', 'target': 'Consulis', 'weight': 1},
                {'source': 'Gaius', 'target': 'Gaius Plinius Secundus', 'weight': 1},
                {'source': 'Quintus', 'target': 'Gaius Plinius Secundus', 'weight': 1},
                {'source': 'Senator', 'target': 'Gaius Plinius Secundus', 'weight': 2},
                {'source': 'Consulis', 'target': 'Gaius Plinius Secundus', 'weight': 1},
            ],
        }
        nodes = NodeEdgeListView()
        data = nodes.get_data()

        for link in expected_dict['links']:
            assert link in data['links']
        for node in expected_dict['nodes']:
            assert node in data['nodes']
        assert len(expected_dict['links']) == len(data['links'])
        assert len(expected_dict['nodes']) == len(data['nodes'])

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
