import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField('email address', blank=False, null=False, unique=True)

    def active_avatar(self) -> str:
        avatar = self.avatar_set.get()
        avatar_url = avatar.file_path.url
        return avatar_url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = str(uuid.uuid4())
        super().save(*args, **kwargs)


def user_avatar_upload(instance, filename):
    return f'{instance.user_id}/{filename}'


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to=user_avatar_upload)
    # file_path = models.ImageField(upload_to='avatars/')

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.file_path.storage, self.file_path.path
        # Delete the model before the file
        super(Avatar, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
