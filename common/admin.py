from django.contrib import admin
from common.models import Citation, Monograph, Article, Section, Contributor, WorkContributor
# Register your models here.

admin.site.register(Citation)
admin.site.register(Contributor)


class WorkContributorInline(admin.TabularInline):
    """Inline admin for WorkContributor through table."""
    model = WorkContributor
    extra = 1


class MonographAdmin(admin.ModelAdmin):

    model = Monograph
    inlines = (WorkContributorInline,)


class ArticleAdmin(admin.ModelAdmin):

    model = Article
    inlines = (WorkContributorInline,)


class SectionAdmin(admin.ModelAdmin):

    model = Section
    inlines = (WorkContributorInline,)


admin.site.register(Monograph, MonographAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Section, SectionAdmin)
