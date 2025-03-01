from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
import pytz
import os

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Incorrect email or password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(pytz.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(pytz.UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        # response.set_cookie(
        #     key='jwt',
        #     value=token,
        #     httponly=True,         # Prevent access by JavaScript
        #     secure=True,          # Use `True` only for HTTPS; set to `False` for development
        #     samesite='None',        # Allow cross-origin cookies for navigation
        #     path="/"  
        # )
        
        response.data = {
                            'msg': 'Login successful!',
                            'data': UserSerializer(user).data,
                            'token': token,
                        }
        return response

class UserView(APIView):
    def get(self, request):
        # token = request.COOKIES.get('jwt')
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id = payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.set_cookie(
            key='jwt',
            value='',
            # httponly=True,         # Prevent access by JavaScript
            secure=True,          # Use `True` only for HTTPS; set to `False` for development
            samesite='None',        # Allow cross-origin cookies for navigation
            path="/"
        )
        response.data = {
                            'msg': 'Logout successful!'
                        }
        return response
