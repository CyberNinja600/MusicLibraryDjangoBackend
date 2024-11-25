from django.urls import path
from .views import AlbumCreateView, AlbumUpdateView, AlbumReadView, AlbumDeleteView, AlbumListView, AlbumAllListView
urlpatterns = [
    path('albums/create', AlbumCreateView.as_view()),
    path('albums/read/<int:id>', AlbumReadView.as_view()),   
    path('albums/edit/<int:id>', AlbumUpdateView.as_view()),
    path('albums/delete', AlbumDeleteView.as_view()),    
    path('albums/list', AlbumListView.as_view()),
    path('albums/all', AlbumAllListView.as_view()),
]
