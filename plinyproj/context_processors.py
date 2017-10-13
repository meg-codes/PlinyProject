from prosopography.forms import SearchForm


def add_search_form(request):
    """Add the search form to all page contexts for the header"""
    search_form = SearchForm()
    search_form.fields
    context_extras = {
        'nav_form': SearchForm(auto_id="nav_%s"),
        'search_form': SearchForm()
    }
    return context_extras
