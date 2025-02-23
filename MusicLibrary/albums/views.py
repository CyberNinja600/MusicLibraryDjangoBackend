from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .services import *
from songs.utils import get_user_from_token

class AlbumCreateView(APIView):
    def post(self, request):
        try:
            uid = get_user_from_token(request)
            if(request.data.get('image')):
                image_url, image_public_id  = upload_image_album(request, uid) 
                response_album = fill_album(request, image_url, image_public_id, uid)
            else:
                response_album = fill_album(request, None, None, uid)
            fill_album_songs(request, response_album['album_id'])

            album = get_album_by_id(request, response_album['album_id'])
            songs = get_album_songs(album.id)
            return Response({"album": AlbumSerializer(album).data, "song": songs}, status=status.HTTP_200_OK)
        
        except AuthenticationFailed as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumReadView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            album = get_album_by_id(request, self.kwargs['id'])
            passed = verify_public(album, get_user_from_token(request))
            if(passed):
                serializer = AlbumSerializer(album) 
                songs = get_album_songs(album.id)
                return Response({"album_data" : serializer.data, "songs": songs}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'error': 'This album is private'}, status=401)
        except AuthenticationFailed as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            uid = get_user_from_token(request)
            album = get_album_by_id(request)
            if(album.created_by_id == uid):
                if(request.data.get('image')):
                    if(album.image_public_id):
                        delete_album_image(album)
                    request.data['image_url'], request.data['image_public_id']  = upload_image_album(request, uid)
                
                serializer_data = update_album_data(request, album)
                if(request.data.get('songs')):
                    songs_update = update_album_songs(request, album.id)
                
                return Response({'status': 'success','data_update' : serializer_data, 'songs_update': songs_update}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failed', 'error': 'You cannot update this album'}, status=401)
            
        except AuthenticationFailed as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumDeleteView(APIView):
    def post(self, request, **kwargs):
        try:
            album = get_album_by_id(request)
            if(get_user_from_token(request) == album.created_by_id):
                delete_album_image(album)
                album.delete()
                return Response({'status': True}, status=status.HTTP_200_OK)
            return Response({'status': False, 'error': 'You cannot delete this album'}, status=401)
        
        except AuthenticationFailed as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumListView(APIView):
    def get(self, request):
        try:
            data = get_my_albums(request, get_user_from_token(request))
            return Response(data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumAllListView(APIView):
    def get(self, request):
        try:
            data = get_all_albums()
            return Response({'status': 'true', 'data': data}, status=status.HTTP_200_OK)
        
        except AuthenticationFailed as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)  
        except Exception as e:
            return Response({'status': 'false', "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)