from .serializers import AlbumSerializer, SongsAlbumSerializer
from .models import *
from django.shortcuts import get_object_or_404
import cloudinary

def fill_album(request, image_url, image_public_id, created_by):
    data = {
        "name": request.data.get('name'),
        "image_url": image_url,
        "image_public_id": image_public_id,
        "listen_count": 0,
        "public": request.data.get('public'),
        "created_by": created_by
    }
    serializer = AlbumSerializer(data=data)
    if serializer.is_valid():
        album = serializer.save()
        return({ 'status': True, 'album_id' : album.id})
    else:
        return({'status': False, 'errors': serializer.errors})
    
def fill_album_songs(request, album_id, update = False):
    for i in range(len(request.data.get('songs').split(','))):
        data = {
            "album_id": album_id,
            "song_id": int((request.data.get('songs').split(','))[i]),
            "sequence": i,
        }
        serializer = SongsAlbumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            if(update):
                continue
            else:
                return({
                    'status': False,
                    'errors': serializer.errors,
                })
    return({'status': serializer.data})
    
def upload_image_album(request, uid):
    img_file = request.data.get('image')
    img_file.seek(0)
    uploaded_img = cloudinary.uploader.upload(img_file, folder = f'album_img/{uid}/')
    return uploaded_img['secure_url'], uploaded_img['public_id']


def get_album_by_id(request, id=None):
    if(id):
        return get_object_or_404(Album, id=id)    
    else:
        return get_object_or_404(Album, id=request.data.get('id'))

def verify_public(album, id):
    if(album.public == 0 and album.created_by_id != id):
        return False
    else:
        return True

def delete_album_image(album):
    album.image_url = None
    cloudinary.api.delete_resources(album.image_public_id, resource_type="image", type="upload")
    album.image_public_id = None
    album.save()
    return('deleted')

def update_album_data(request, album):
    serializer = AlbumSerializer(album, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return serializer.data

def update_album_songs(request, id):
    Songs_Album.objects.filter(album_id=id).delete()
    response = fill_album_songs(request, id, True)
    return response

def get_my_albums(request,id):
    albums = Album.objects.filter(created_by_id=id)
    serializer = AlbumSerializer(albums, many=True)
    return serializer.data

def get_album_songs(album_id):
    songs = Songs_Album.objects.filter(album_id=album_id)
    serializer = SongsAlbumSerializer(songs, many=True)
    return serializer.data

def get_all_albums():
    serializer = AlbumSerializer(Album.objects.all(), many=True)
    return serializer.data