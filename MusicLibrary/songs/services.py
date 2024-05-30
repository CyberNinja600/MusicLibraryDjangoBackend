from .serializers import SongsSerializer, ArtistSongsSerializer
from .models import Songs, Artist_Songs
from django.shortcuts import get_object_or_404
import cloudinary

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

def remove_artists_songs(song_id):
    Artist_Songs.objects.filter(song_id=song_id).delete()

def get_song_by_id(song_id):
    return SongsSerializer(Songs.objects.get(id=song_id)).data

def delete_son_by_id(song_id):
    return Songs.objects.filter(id=song_id).delete()

def get_my_uploads(uid):
    songs = Songs.objects.filter(artist_songs__user_id=uid)
    return SongsSerializer(songs, many=True).data

def failed_upload():
    return True

def update_song_data(request, uid):
    song = get_object_or_404(Songs, id=request.data.get('id'))
    name = request.data.get('name', song.name)
    description = request.data.get('description', song.description)
    image_url, image_public_id, image_updated = update_song_url(song, request, uid, False)

    song.name = name
    song.description = description
    song.image_url = image_url
    song.image_public_id = image_public_id
    song.save()

    return({'data' : SongsSerializer(song).data, 'image_updated': image_updated})

def update_song_url(song, request, uid, image_updated = False):
    if 'image' in request.data:
        delete_old_image_song(song)
        image_url, image_public_id = upload_image_song(request, uid)
        image_updated = True
    else:
        image_url = song.image_url
        image_public_id = song.image_public_id
    return image_url, image_public_id, image_updated

def delete_old_image_song(song):
    cloudinary.api.delete_resources(song.image_public_id, resource_type="image", type="upload")

def upload_image_song(request, uid):
    img_file = request.data.get('image')
    img_file.seek(0)
    uploaded_img = cloudinary.uploader.upload(img_file, folder = f'songs_img/{uid}/')
    return uploaded_img['secure_url'], uploaded_img['public_id']