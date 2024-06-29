from django.urls import path
from .views import AlbumCreateView, AlbumUpdateView, AlbumReadView, AlbumDeleteView, AlbumListView
urlpatterns = [
    path('album/create', AlbumCreateView.as_view()),
    path('album/read/<int:id>', AlbumReadView.as_view()),   
    path('album/edit/<int:id>', AlbumUpdateView.as_view()),
    path('album/delete', AlbumDeleteView.as_view()),    
    path('album/list', AlbumListView.as_view()),
]
