from django.db import models
from django.conf import settings

# 開発者情報モデル
class Developer(models.Model):
    artist_id = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='developers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.artist_name

# アプリ情報モデル
class Application(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='applications')
    track_name = models.CharField(max_length=255)
    track_url = models.URLField(max_length=500)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    artworkUrl512 = models.URLField(max_length=500,blank=True, null=True)
    artworkUrl100 = models.URLField(max_length=500, blank=True, null=True)
    artworkUrl60 = models.URLField(max_length=500, blank=True, null=True)
    screenshotUrls = models.JSONField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.track_name
