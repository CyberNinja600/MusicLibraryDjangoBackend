from django.urls import path
from .views import SongsCreateView
urlpatterns = [
    path('songs/add', SongsCreateView.as_view()),
]
