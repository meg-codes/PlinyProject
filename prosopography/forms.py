from django import forms


class SearchForm(forms.Form):
    nomina = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['nomina'].widget.attrs.update({'class': 'typeahead'})
