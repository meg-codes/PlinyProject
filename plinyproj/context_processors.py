from prosopography.forms import SearchForm


def add_search_form(request):
    """Add the search form to all page contexts for the header"""
    context_extras = {
        'search_form': SearchForm()
    }
    return context_extras
