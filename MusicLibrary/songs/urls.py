from django.urls import path
from .views import SongsCreateView, SongsDeleteView, SongsMyUploadsView, SongsAllUploadsView, SongsUpdateView
urlpatterns = [
    path('songs/add', SongsCreateView.as_view()),
    path('songs/delete', SongsDeleteView.as_view()),
    path('songs/update', SongsUpdateView.as_view()),
    path('songs/my-uploads', SongsMyUploadsView.as_view()),
    path('songs/all-uploads', SongsAllUploadsView.as_view()),
]
