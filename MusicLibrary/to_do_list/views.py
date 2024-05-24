from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ToDoListSerializer
from users.models import User
from django.core.exceptions import ObjectDoesNotExist

import jwt


class ToDoListCreateView(APIView):
    def post(self, request):
        user = get_user_from_token(request)
        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'msg': 'Task created successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoListRetrieveView(APIView):
    def post(self, request):
        user = get_user_from_token(request)
        tasks = user.todolist_set.all()
        serializer = ToDoListSerializer(tasks, many=True)
        return Response(serializer.data)


class ToDoListDeleteTaskView(APIView):
    def post(self, request):
        try:
            user = get_user_from_token(request)  
            task = user.todolist_set.get(id=request.data.get("task_id"))
            task.delete()
            return Response({'msg': 'Task deleted successfully!'})
        
        except:
            return Response({'msg': 'Task does not exist!'})


class ToDoListUpdateTaskView(APIView):
    def post(self, request):            
        try:
            user = get_user_from_token(request)  
            task = user.todolist_set.filter(id=request.data.get('id'))
            
            if task.exists():
                task.update(**request.data)
                return Response({'msg': 'Task updated successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_user_from_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
        return User.objects.get(id=user_id)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except ObjectDoesNotExist:
        raise AuthenticationFailed('User not found')