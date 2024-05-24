from django.urls import path
from .views import ToDoListCreateView, ToDoListRetrieveView, ToDoListDeleteTaskView, ToDoListUpdateTaskView
urlpatterns = [
    path('to-do/add', ToDoListCreateView.as_view()),
    path('to-do/tasks', ToDoListRetrieveView.as_view()),
    path('to-do/delete', ToDoListDeleteTaskView.as_view()),
    path('to-do/update', ToDoListUpdateTaskView.as_view())
]
