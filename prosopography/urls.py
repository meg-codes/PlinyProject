from django.conf.urls import url
from .views import PersonListView, person_autocomplete
urlpatterns = [
    url(r'^$', PersonListView.as_view(), name='search'),
    url(r'^autocomplete', person_autocomplete, name='autocomplete'),
]
