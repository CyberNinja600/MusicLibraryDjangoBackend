from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import *
from songs.utils import get_user_from_token

class AlbumCreateView(APIView):
    def post(self, request):
        uid = get_user_from_token(request)
        image_url, image_public_id  = upload_image_album(request, uid) 
        response = fill_album(request, image_url, image_public_id, uid)
        response = fill_album_songs(request, response['album_id'])
        return Response(response, status=status.HTTP_200_OK)
       