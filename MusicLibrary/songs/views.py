import cloudinary

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import  get_user_from_token
from .mixins import FileValidationMixin
from .services import *

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
                uploaded_img = cloudinary.uploader.upload(img_file, folder = f'songs_img/{get_user_from_token(request)}/')

                song_id = fill_song(request, uploaded_file['secure_url'], uploaded_file['public_id'], uploaded_img['secure_url'], uploaded_img['public_id'])
                if(song_id['status'] == True):
                    fill_artist_songs(request.data.get('user_ids').split(','), song_id['id'])
                    return Response({'status': 'true',"message": "File uploaded successfully", "song_url": uploaded_file['secure_url'], "image_url": uploaded_img['secure_url']}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status': 'false', "error": "Failed to upload song."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'status': 'false', "error": 'Failed Validation', 'song_validation': validation_song, 'image_validation': validation_img}, status=status.HTTP_400_BAD_REQUEST)


class SongsDeleteView(APIView):
    def post(self, request):
        try:
            song = get_song_by_id(request.data.get('song_id'))
            song_delete_result = cloudinary.api.delete_resources(song.get('song_public_id'), resource_type="video", type="upload")
            image_delete_result = cloudinary.api.delete_resources(song.get('image_public_id'), resource_type="image", type="upload")
            delete_son_by_id(request.data.get('song_id'))
            return Response({'status': 'true', "message": "File Deleted successfully", "data" : song, "image_data": image_delete_result, "song_data": song_delete_result}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status': 'false',"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SongsMyUploadsView(APIView):
    def get(self, request):
        try:
            data = get_my_uploads(get_user_from_token(request))
            return Response({'status': 'true', 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)