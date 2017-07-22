from django.views.generic import ListView
from django.http.response import JsonResponse
from django import forms

from .models import Person


def person_autocomplete(request):

    query = request.GET.get('q')
    if query:
        people = Person.objects.filter(
                 nomina__icontains=query).values_list('nomina', flat=True)
        return JsonResponse(list(people), safe=False)
    return JsonResponse({})


class SearchForm(forms.Form):
    nomina = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['nomina'].widget.attrs.update({'class': 'typeahead'})

class PersonListView(ListView):
    """View to display results of a search for all
    :class:`prosopography.models.Person` instances in the database with filters"""
    model = Person
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        if not self.request.GET.get('nomina', None):
            context['object_list'] = None
        context['form'] = SearchForm()
        params = []
        for query in self.request.GET:
            if query != 'page':
                params.append('%s=%s' % (query, self.request.GET[query]))
        context['saved_query'] = "&".join(params)
        return context

    def get_queryset(self):
        nomina = self.request.GET.get('nomina', None)
        if not nomina:
            return Person.objects.none()

        people = super(PersonListView, self).get_queryset()
        return people.filter(nomina__icontains=nomina)
