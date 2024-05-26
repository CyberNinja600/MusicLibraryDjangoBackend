from django.db import models
from users.models import User


class Songs(models.Model):
    name = models.CharField(max_length=150)
    song_url = models.TextField(max_length=600)
    song_public_id = models.TextField(max_length=500)
    image_url = models.TextField(max_length=600)
    image_public_id = models.TextField(max_length=500)
    description = models.TextField(max_length=1500)
    listen_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Artist_Songs(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Songs, on_delete=models.CASCADE)
    sequence = models.IntegerField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist.name + " - " + self.song.name