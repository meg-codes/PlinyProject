from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('people', views.PersonListView.as_view(), name='people'),
    path('people/autocomplete', views.PersonAutocompleteView.as_view(), name='autocomplete'),
    path('people/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
    path('posts', views.PostListView.as_view(), name='posts')
]