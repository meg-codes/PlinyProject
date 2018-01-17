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


def person_autocomplete(request):
    """Autocomplete view public-facing for nomina autocomplete"""
    query = request.GET.get('q')
    if query:
        people = Person.objects.filter(
                 nomina__icontains=query).values_list('nomina', flat=True)
        return JsonResponse(list(people), safe=False)
    return JsonResponse({})


class PersonDetailView(DetailView):
    """Get the detail view of a person based on pk and redirect to proper slug."""
    model = Person

    def get_object(self, queryset=None):
        """Override to ignore slug lookups because it's actually a property"""
        queryset = self.get_queryset()
        if 'id' in self.kwargs and self.kwargs['id']:
            return queryset.get(pk=self.kwargs['id'])

    def render_to_response(self, context, **kwargs):
        """Override to redirect to proper slug if nomina changes"""
        # if these don't line up, it's probably a malformed or changed slug
        # so redirect to the right slug.
        if self.object.get_absolute_url() != self.request.path:
            return redirect(self.object)
        return super(PersonDetailView, self).render_to_response(context, **kwargs)


class PersonListView(ListView):
    """View to display results of a search for all
    :class:`prosopography.models.Person` instances in the database with filters"""
    model = Person
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        params = []
        for query in self.request.GET:
            if query != 'page':
                params.append('%s=%s' % (query, self.request.GET[query]))
        context['saved_query'] = "&" + '&'.join(params)
        return context

    def get_queryset(self):
        """
        Get queryset for people and filter by query string params
        """
        people = super(PersonListView, self).get_queryset()
        filters = self.request.GET
        nomina = filters.get('nomina', '')
        filter_list = []
        if filters.get('senatorial'):
            filter_list.append(people.filter(senatorial='Y'))
        if filters.get('equestrian'):
            filter_list.append(people.filter(equestrian='Y'))
        if filters.get('citizen'):
            filter_list.append(people.filter(
                    equestrian__in=['N', 'U'],
                    senatorial__in=['N', 'U'],
                    citizen='Y'
                )
            )
        filter_list = list(filter(None, filter_list))
        if filter_list:
            people = reduce(ior, filter_list)

        return people.filter(nomina__icontains=nomina).order_by('nomina')


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
            group = 1
        if person.equestrian == Y:
            group = 2
        if person.senatorial == Y:
            group = 3
        if person.consular == Y:
            group = 4
        return group

    def get_data(self):
        """Get data for people and their relationships and format for d3.js"""
        people = self.get_queryset()
        # filter out a nodelist in the format d3v4 expects
        node_edge_dict = {
            'nodes': [{'id': 'Gaius Plinius Secundus', 'group': 9}],
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
