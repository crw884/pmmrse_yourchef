from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    profile_image = models.ImageField(upload_to="static/img", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='Группа к которой принадлежит',
        related_name='custom_users_groups',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Разрешения юзера',
        related_name='custom_users_permissions',
        related_query_name='user',
    )
    def __str__(self):
        return self.username
