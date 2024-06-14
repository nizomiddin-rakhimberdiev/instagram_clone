from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=13)
    profile_picture = models.ImageField(upload_to='media/profile_pictures/', null=True, blank=True, default='media/profile_pictures/avatar.png')

    def set_password(self, raw_password):
        super().set_password(raw_password)
    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} : {self.content}"
