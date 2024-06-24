from .serializers import AlbumSerializer, SongsAlbumSerializer
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
    
def fill_album_songs(request, album_id):
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
            return({
                'status': False,
                'errors': serializer.errors,
            })
    return({'status': True})
    
def upload_image_album(request, uid):
    img_file = request.data.get('image')
    img_file.seek(0)
    uploaded_img = cloudinary.uploader.upload(img_file, folder = f'album_img/{uid}/')
    return uploaded_img['secure_url'], uploaded_img['public_id']