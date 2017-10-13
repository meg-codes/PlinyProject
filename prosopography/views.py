from dal import autocomplete
from functools import reduce
from operator import ior

from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.http.response import JsonResponse

from .forms import SearchForm
from .models import Person


@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class PersonAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        """Get a query set to return for DAL autocomplete in admin"""
        return Person.objects.filter(nomina__icontains =self.q)


def person_autocomplete(request):

    query = request.GET.get('q')
    if query:
        people = Person.objects.filter(
                 nomina__icontains=query).values_list('nomina', flat=True)
        return JsonResponse(list(people), safe=False)
    return JsonResponse({})


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
