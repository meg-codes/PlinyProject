from django.contrib import admin
from .models import Letter, Topic, Correspondent


class CorrespondentInline(admin.TabularInline):
    model = Correspondent.letters_to.through


class LetterAdmin(admin.ModelAdmin):
    model = Letter
    inlines = [CorrespondentInline]
    fields = ('book', 'letter', 'topics', 'date')


admin.site.register(Letter, LetterAdmin)
admin.site.register(Topic)
