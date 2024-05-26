from django.urls import path
from .views import SongsCreateView, SongsDeleteView
urlpatterns = [
    path('songs/add', SongsCreateView.as_view()),
    path('songs/delete', SongsDeleteView.as_view()),
]
