from django.urls import path
from .views import MusicPlayerView

urlpatterns = [
    path('music-player/play/<int:song_id>', MusicPlayerView.as_view()),
]
