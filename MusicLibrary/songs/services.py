from .serializers import SongsSerializer, ArtistSongsSerializer
from .models import Songs, Artist_Songs

def fill_song(request, song_url, song_public_id ,image_url, image_public_id):
    data = {
        "name": request.data.get('name'),
        "song_url": song_url,
        "song_public_id": song_public_id,
        "image_url": image_url,
        "image_public_id": image_public_id,
        "description": request.data.get('description')
    }

    serializer = SongsSerializer(data=data)
    if serializer.is_valid():
        song = serializer.save()
        return({ 'status': True, 'id' : song.id})
    else:
        failed_upload()
        return({'status': False})

def fill_artist_songs(user_ids, song_id):
    for index, user_id in enumerate(user_ids):
        data = {
            "user_id": user_id,
            "song_id": song_id,
            "sequence": index
        }
        serializer = ArtistSongsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            failed_upload()
            return({
                'status': False,
            })
    return True

def get_song_by_id(song_id):
    return SongsSerializer(Songs.objects.get(id=song_id)).data

def delete_son_by_id(song_id):
    return Songs.objects.filter(id=song_id).delete()

def get_my_uploads(uid):
    songs = Songs.objects.filter(artist_songs__user_id=uid)
    return SongsSerializer(songs, many=True).data

def failed_upload():
    return True