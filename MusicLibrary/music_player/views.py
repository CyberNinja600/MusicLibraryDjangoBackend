from rest_framework.views import APIView
from rest_framework.response import Response

from songs.serializers import SongsSerializer
from songs.utils import  get_user_from_token
from songs.models import Songs


class MusicPlayerView(APIView):
    def get(self, request, song_id):
        self.authenticate(request)
        validate = self.validate_id(song_id)
        print(validate)
        if validate['status'] == True:
            return Response(validate, status=200)
        return Response({'status': 'false'}, status=400)
    
    def authenticate(self, request):
        return get_user_from_token(request)
    
    def validate_id(self, song_id):
        song = Songs.objects.filter(id=song_id).first()
        if song is not None:
            return self.paginate_data(song)
        return {'status': False}
    
    def paginate_data(self, song):
        next_song = Songs.objects.filter(id__gt=song.id).order_by('id').first()
        prev_song = Songs.objects.filter(id__lt=song.id).order_by('-id').first()
        
        result = {
            'status': True,
            'current_song': SongsSerializer(song).data,
            'next_page': SongsSerializer(next_song).data if next_song else None,
            'prev_page': SongsSerializer(prev_song).data if prev_song else None
        }
        return result