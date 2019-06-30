from django.conf.urls import url
from .views import (PersonAutoComplete, NodeEdgeListView,
                    SocialClassView)

app_name = 'prosopography'

urlpatterns = [
    url(r'^dal-autocomplete/$', PersonAutoComplete.as_view(),
        name='dal-autocomplete'),
    url(r'^nodes.json$', NodeEdgeListView.as_view(), name='nodes'),
    url(r'^social_class.json$', SocialClassView.as_view(), name='classes')
]
