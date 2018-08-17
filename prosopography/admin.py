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
    model = Person.mentioned_in.through
    show_change_link = True
    verbose_name_plural = "Letters in which Pliny mentions this person"
    extra = 1


class RelationshipInline(admin.TabularInline):
    model = Relationship
    fk_name = 'from_person'


class CorrespondentAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline, LettersToInline, MentionedInline, AKAInline]
    model = Person
    list_display = ('nomina', 'gender', 'from_comum',
                    'citizen', 'equestrian', 'senatorial',
                    'consular', 'birth', 'death', 'cos', 'cos_suff', 'floruit',
                    'certainty_of_id', 'notes')
    list_filter = ('citizen', 'equestrian', 'senatorial', 'consular', 'cos',
                   'certainty_of_id')
    search_fields = ('nomina', 'notes')
    filter_horizontal = ('citations',)
    fields = (
        'nomina',
        'gender',
        'from_comum',
        ('citizen', 'equestrian', 'senatorial', 'consular'),
        ('birth', 'death', 'cos', 'cos_suff' , 'floruit'),
        'certainty_of_id',
        'notes',
        'citations',
    )

    exclude = ['letters_to', 'mentioned_in']


admin.site.register(Person, CorrespondentAdmin)
admin.site.register(Relationship)
