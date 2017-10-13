from dal import autocomplete
from django import forms
from django.contrib import admin
from .models import Letter, Topic, Person


class PersonInlineForm(forms.ModelForm):
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
    model = Person.letters_to.through
    form = PersonInlineForm


class LetterAdmin(admin.ModelAdmin):
    model = Letter
    inlines = [PersonInline]
    fields = ('book', 'letter', 'topics', 'date')
    search_fields = ('book', 'letter', 'letters_to__nomina')
    list_filter = ('book',)

admin.site.register(Letter, LetterAdmin)
admin.site.register(Topic)
