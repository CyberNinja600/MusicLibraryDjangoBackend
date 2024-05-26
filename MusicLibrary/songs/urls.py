from django.urls import path
from .views import SongsCreateView, SongsDeleteView, SongsMyUploadsView
urlpatterns = [
    path('songs/add', SongsCreateView.as_view()),
    path('songs/delete', SongsDeleteView.as_view()),
    path('songs/my-uploads', SongsMyUploadsView.as_view())
]
