from rest_framework import serializers
from .models import Album, Songs_Album

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name', 'image_url' ,'image_public_id', 'listen_count', 'public', 'created_by', 'created_at', 'updated_at']

class SongsAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs_Album
        fields = ['album_id', 'song_id' ,'sequence', 'created_at', 'updated_at']