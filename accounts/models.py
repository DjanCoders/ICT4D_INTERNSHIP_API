from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    avatar = models.ImageField(default='default_avatar.png', upload_to='profile_images/')
    bio = models.TextField(blank=True)
    is_internee = models.BooleanField(default=False)
