from django.contrib import admin
from .models import Person, Relationship, AKA


class AKAInline(admin.TabularInline):
    model = AKA
    extra = 1


class LettersToInline(admin.TabularInline):
    model = Person.letters_to.through
    verbose_name_plural = "Letters of Pliny to this Person"
    show_change_link = True
    extra = 1


class MentionedInline(admin.TabularInline):
    model = Person.letters_to.through
    verbose_name_plural = "Letters in which Pliny mentions this person"
    extra = 1


class CorrespondentAdmin(admin.ModelAdmin):
    inlines = [LettersToInline, MentionedInline, AKAInline]
    model = Person
    fields = (
        'nomina',
        'gender',
        ('citizen', 'equestrian', 'senatorial', 'consular'),
        ('birth', 'death', 'cos', 'floruit'),
        'certainty_of_id',
        'notes',
    )
    exclude = ['letters_to', 'mentioned_in']


admin.site.register(Person, CorrespondentAdmin)
admin.site.register(Relationship)
