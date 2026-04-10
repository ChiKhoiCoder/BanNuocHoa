"""Avatar upload model and helpers."""
from django.db import models
from django.conf import settings


class Avatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatars"

    def __str__(self):
        return f"Avatar for {self.user}"


def avatar_upload_path(instance, filename):
    # TODO: customize path (e.g., user id / uuid)
    return f"avatars/{instance.user.id}/{filename}"
