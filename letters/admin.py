from django.contrib import admin
from .models import Letter, Topic, Person


class PersonInline(admin.TabularInline):
    model = Person.letters_to.through

class LetterAdmin(admin.ModelAdmin):
    model = Letter
    inlines = [PersonInline]
    fields = ('book', 'letter', 'topics', 'date')


admin.site.register(Letter, LetterAdmin)
admin.site.register(Topic)
