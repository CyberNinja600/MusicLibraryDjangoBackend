from rest_framework import serializers
from .models import Songs, Artist_Songs

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ['id','name', 'song_url', 'song_public_id' ,'image_url', 'image_public_id' ,'description', 'created_at', 'updated_at']

class ArtistSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist_Songs
        fields = ['user_id', 'song_id' ,'sequence', 'created_at', 'updated_at']
