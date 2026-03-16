import os
import uuid
from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    """
    Генерирует путь для сохранения файла:
    media/user_<id>/<uuid>.<ext>
    """
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(f"user_{instance.owner.id}", new_filename)

class File(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='files'
    )
    original_name = models.CharField(max_length=255)
    stored_name = models.CharField(max_length=255, unique=True)
    size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True)
    file = models.FileField(upload_to=user_directory_path)
    special_link_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.stored_name:
            self.stored_name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            storage = self.file.storage
            if storage.exists(self.file.name):
                storage.delete(self.file.name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.original_name