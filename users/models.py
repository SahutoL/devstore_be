from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Djangoのデフォルトユーザーを拡張したカスタムユーザーモデル。
    """

    # 既存のグループ・権限との競合を防ぐため related_name を設定
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True
    )

    def __str__(self):
        return self.username

class PushSubscription(models.Model):
    """
    各ユーザーのWeb Push通知用購読情報
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.TextField()
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} subscription"
