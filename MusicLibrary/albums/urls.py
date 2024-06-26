from django.urls import path
from .views import AlbumCreateView, AlbumEditView
urlpatterns = [
    path('album/create', AlbumCreateView.as_view()),
    path('album/edit', AlbumEditView.as_view()),
]
