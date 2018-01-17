from django.conf.urls import url
from .views import (PersonListView, person_autocomplete, NodeEdgeListView)

urlpatterns = [
    url(r'^$', PersonListView.as_view(), name='search'),
    url(r'^autocomplete/$', person_autocomplete, name='autocomplete'),
    url(r'^nodes.json$', NodeEdgeListView.as_view(), name='nodes'),

]
