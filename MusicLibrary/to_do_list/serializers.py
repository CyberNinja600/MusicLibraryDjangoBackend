from rest_framework import serializers
from .models import ToDoList

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ['id', 'task' ,'completed', 'created_at', 'updated_at', 'start_date', 'end_date']
        read_only_fields = ['user']