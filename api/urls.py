from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('people', views.PersonListView.as_view(), name='people'),
    path('posts', views.PostListView.as_view(), name='posts')
]