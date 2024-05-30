from django.db import models
from users.models import User
from songs.models import Songs

class Album(models.Model):
    name = models.CharField(max_length=150)
    image_url = models.TextField(max_length=600)
    image_public_id = models.TextField(max_length=500)
    listen_count = models.IntegerField(default=0)
    public = models.IntegerField(default=1,)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Songs_Album(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Songs, on_delete=models.CASCADE)
    sequence = models.IntegerField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.album_id + " - " + self.song_id