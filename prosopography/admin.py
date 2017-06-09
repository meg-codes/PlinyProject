from django.contrib import admin
from .models import Correspondent, Relationship, AKA
from letters.models import Letter


class AKAInline(admin.TabularInline):
    model = AKA
    extra = 1


class LettersToInline(admin.TabularInline):
    model = Correspondent.letters_to.through
    verbose_name_plural = "Letters of Pliny to this Person"
    show_change_link = True
    extra = 1


class MentionedInline(admin.TabularInline):
    model = Correspondent.letters_to.through
    verbose_name_plural = "Letters in which Pliny mentions this person"
    extra = 1


class CorrespondentAdmin(admin.ModelAdmin):
    inlines = [LettersToInline, MentionedInline, AKAInline]
    model = Correspondent
    fields = (
        'nomina',
        'gender',
        ('citizen', 'equestrian', 'senatorial', 'consular'),
        ('birth', 'death', 'cos', 'floruit'),
        'certainty_of_id',
        'notes',
    )
    exclude = ['letters_to', 'mentioned_in']


admin.site.register(Correspondent, CorrespondentAdmin)
admin.site.register(Relationship)
