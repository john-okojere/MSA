from django.db import models
from .manage import UserManager
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='email address', unique=True,
        error_messages={
            'unique': "This email has been used already",
        },
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    update_fields = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'


    objects = UserManager()
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.email)
