from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager

# Create your models here.

# custom superuser
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Set role ke 'admin'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role=admin.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser (AbstractUser):
    ROLE_CHOICES = (
        ('buyer','pembeli'),
        ('seller','penjual'),
        ('admin','admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='buyer',verbose_name='Role')
    no_telp = models.CharField(max_length=20, default='+6285210000000')
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s@./+/-_]*$',  # Mengizinkan spasi dengan regex
                message='Username hanya boleh berisi huruf, angka, dan karakter khusus seperti spasi, @, ., +, -, /, _.'
            ),
        ]
    )

    objects = CustomUserManager()
