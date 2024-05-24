from .serializers import SongsSerializer, ArtistSongsSerializer

def fill_song(request, song_url, image_url):
    data = {
        "name": request.data.get('name'),
        "song_url": song_url,
        "image_url": image_url,
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

def failed_upload():
    return True