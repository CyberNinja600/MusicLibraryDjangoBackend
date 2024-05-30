from rest_framework import serializers
from .models import Songs, Artist_Songs, User

class ArtistSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist_Songs
        fields = ['user_id', 'song_id' ,'sequence', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ArtistRelationSongsSerializer(serializers.ModelSerializer):
    details = UserSerializer(source='user_id', read_only=True)
    class Meta:
        model = Artist_Songs
        fields = ['sequence', 'details']

class SongsSerializer(serializers.ModelSerializer):
    artists = ArtistRelationSongsSerializer(source='artist_songs_set', many=True, read_only=True)
    class Meta:
        model = Songs
        fields = ['id','name', 'song_url', 'song_public_id' ,'image_url', 'image_public_id' ,'description', 'created_at', 'updated_at', 'artists']