from functools import reduce
from operator import ior

from dal import autocomplete
from django.contrib.auth.decorators import user_passes_test
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .forms import SearchForm
from .models import Person, SocialField


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class PersonAutoComplete(autocomplete.Select2QuerySetView):
    """DAL autocomplete for use in the Django-admin"""
    def get_queryset(self):
        """Get a query set to return for DAL autocomplete in admin"""
        people = Person.objects.all()
        return people.filter(nomina__istartswith=self.q).order_by('nomina')


class NodeEdgeListView(ListView):
    """Provide node-edge json for use """
    model = Person

    def render_to_json_response(self, **kwargs):
        """Contextless rendering of queryset from get_data"""
        return JsonResponse(self.get_data())

    def assign_class(self, person):
        """Assign classes to a group based on fields"""
        # NOTE: This is dumb but very safe that the group will be set in some way
        Y = SocialField.DEFINITE
        group = 0
        if person.citizen == Y:
            group = 'citizen' 
        if person.equestrian == Y:
            group = 'equestrian'
        if person.senatorial == Y:
            group = 'senatorial'
        if person.consular == Y:
            group = 'consular'
        return group

    def get_data(self):
        """Get data for people and their relationships and format for d3.js"""
        people = self.get_queryset()
        # filter out a nodelist in the format d3v4 expects
        node_edge_dict = {
            'nodes': [{'id': 'Gaius Plinius Secundus', 'group': 'consular'}],
            'links': [],
        }
        # generate nodes
        for person in people:
            node_edge_dict['nodes'].append(
                {'id': person.nomina, 'group': self.assign_class(person)}
            )
            # add all links to pliny based on number of letters
            node_edge_dict['links'].append(
                {
                    'source': 'Gaius Plinius Secundus',
                    'target': person.nomina,
                    'weight': (
                        person.letters_to.count() +
                        person.mentioned_in.count()
                    ),
                }
            )

        # make all Pliny links reciprocal
        reciprocal_links = []
        for link in node_edge_dict['links']:
            reciprocal_links.append({
                'source': link['target'],
                'target': link['source'],
                'weight': link['weight']
            })
        node_edge_dict['links'] += reciprocal_links

        """
        # Pulled for now not needed for ego 1.5 model
        # relationships should be reciprocal if they need to be already
        for relationship in Relationship.objects.all():
            node_edge_dict['links'].append({
                'source': relationship.from_person.nomina,
                'target': relationship.to_person.nomina,
                'weight': 1,
            })
        comumienses = Person.objects.filter(from_comum=True)

        for outer in comumienses:
            for inner in comumienses:
                node_edge_dict['links'].append({
                    'source': outer.nomina,
                    'target': inner.nomina,
                    'weight': 1
                })

        # group all relationships by common source and target if they
        # aren't already
        grouped_edge_list = []
        for outer in node_edge_dict['links']:
            for inner in node_edge_dict['links']:
                if (outer['source'] == inner['source']) and \
                        (outer['target'] == inner['target']):
                    outer['weight'] = outer['weight'] + inner['weight']
            grouped_edge_list.append(outer)
        node_edge_dict['links'] = [dict(t) for t in set([tuple(d.items())
                                   for d in grouped_edge_list])]
        """
        return node_edge_dict

    def render_to_response(self, context, **kwargs):
        return self.render_to_json_response()


class SocialClassView(ListView):
    model = Person

    def render_to_json_response(self, **kwargs):
        """Contextless rendering of queryset from get_data"""
        return JsonResponse(self.get_data())

    def get_data(self):
        people = self.get_queryset()

        book = self.request.GET.get('q', '')
        if book:
            try:
                book = int(book)
                people = people.filter(letters_to__book=book)
            except ValueError:
                pass
        # data for Chart.js
        data = {
            'datasets': [{
                # get people as senatorial, equestrian, and citizen
                'data': [
                    people.filter(senatorial='Y').count(),
                    people.filter(equestrian='Y', senatorial='N').count(),
                    people.filter(citizen='Y',
                                  equestrian='N', senatorial='N').count()
                    ],
                'backgroundColor': [
                    'rgb(127, 63, 191)',
                    'rgb(191, 63, 63)',
                    'rgb(63, 191, 191)'
                ],

            }],
            'labels': [
                'Senatorial',
                'Equestrian',
                'Citizen',
            ]
        }
        return data

    def render_to_response(self, context, **kwargs):
        return self.render_to_json_response()
