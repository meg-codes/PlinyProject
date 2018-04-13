from django.contrib import admin
from common.models import Citation, Monograph, Article, Section
# Register your models here.
models = [Citation, Monograph, Article, Section]
for model in models:
    admin.site.register(model)
