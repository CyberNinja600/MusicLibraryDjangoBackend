from django.urls import path
from .views import AlbumCreateView
urlpatterns = [
    path('album/create', AlbumCreateView.as_view()),
]
