from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import *
from songs.utils import get_user_from_token

class AlbumCreateView(APIView):
    def post(self, request):
        uid = get_user_from_token(request)
        if(request.data.get('image')):
            image_url, image_public_id  = upload_image_album(request, uid) 
            response = fill_album(request, image_url, image_public_id, uid)
        else:
            response = fill_album(request, None, None, uid)
        response = fill_album_songs(request, response['album_id'])
        return Response(response, status=status.HTTP_200_OK)

class AlbumEditView(APIView):
    def post(self, request):
        uid = get_user_from_token(request)
        album = get_album_by_id(request)
        if(request.data.get('image')):
            if(album.image_public_id):
                delete_album_image(album)
            request.data['image_url'], request.data['image_public_id']  = upload_image_album(request, uid)
        
        serializer_data = update_album_data(request, album)
        
        if(request.data.get('songs')):
            songs_update = update_album_songs(request, album.id)
        
        return Response({'data_update' : serializer_data, 'songs_update': songs_update}, status=status.HTTP_200_OK)

       