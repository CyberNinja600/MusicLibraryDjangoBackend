from rest_framework import serializers
from .models import Songs, Artist_Songs

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ['name', 'song_url' ,'image_url', 'description', 'created_at', 'updated_at']

class ArtistSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist_Songs
        fields = ['user_id', 'song_id' ,'sequence', 'created_at', 'updated_at']
