from dal import autocomplete
from django import forms
from django.contrib import admin
from letters.models import Letter, Topic
from prosopography.models import Person


class PersonInlineForm(forms.ModelForm):
    """Configure inline admin form for :class:`prosopography.models.Person` """
    class Meta:
        model = Person.letters_to.through
        fields = ('__all__')
        widgets = {
                'person': autocomplete.ModelSelect2(
                            url='people:dal-autocomplete',
                            attrs={
                                'data-placeholder': 'Type to search...',
                                'data-minimum-input-length': 2,
                            }
                          ),

                }


class PersonInline(admin.TabularInline):
    """:class:`prosopography.models.Person` admin inline for M2M."""
    model = Person.letters_to.through
    form = PersonInlineForm


class LetterAdmin(admin.ModelAdmin):
    """ModelAdmin for :class:`letters.models.Letter`"""
    model = Letter
    inlines = [PersonInline]
    fields = ('book', 'letter', 'topics', 'date', 'citations')
    search_fields = ('book', 'letter', 'letters_to__nomina')
    list_filter = ('book',)
    filter_horizontal = ('citations',)


admin.site.register(Letter, LetterAdmin)
admin.site.register(Topic)
