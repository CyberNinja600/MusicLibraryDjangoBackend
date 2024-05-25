from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from users.models import User
from .serializers import SongsSerializer, ArtistSongsSerializer

import cloudinary
import jwt
import magic
from PIL import Image
from io import BytesIO

from .utils import  get_user_from_token
from .mixins import FileValidationMixin
from .services import fill_song, fill_artist_songs

class SongsCreateView(APIView, FileValidationMixin):
    def post(self, request):
        
        song_file = request.data.get('song')
        img_file = request.data.get('image')
        validation, validation_song, validation_img = self.validate_files(song_file, img_file)
        
        if validation:
            try:
                song_file.seek(0)
                img_file.seek(0)
                
                uploaded_file =cloudinary.uploader.upload(song_file, resource_type='video', folder = f'songs/{get_user_from_token(request)}/')
                upload_img = cloudinary.uploader.upload(img_file, folder = f'songs_img/{get_user_from_token(request)}/')

                song_id = fill_song(request, uploaded_file['secure_url'], upload_img['secure_url'])
                if(song_id['status'] == True):
                    fill_artist_songs(request.data.get('user_ids').split(','), song_id['id'])
                    return Response({"message": "File uploaded successfully", "song_url": uploaded_file['secure_url'], "image_url": upload_img['secure_url']}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Failed to upload song."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"error": 'Failed Validation', 'song_validation': validation_song, 'image_validation': validation_img}, status=status.HTTP_400_BAD_REQUEST)


class SongDeleteView(APIView):
    def post(self, request):
        return True