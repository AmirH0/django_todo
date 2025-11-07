from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **ext):
        if not email:
            raise ValueError("email is required")
        email_n = self.normalize_email(email)
        user = self.model(email=email_n, **ext)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **ext):
        ext.setdefault("is_admin", True)
        ext.setdefault("is_superuser", True)

        if ext.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if ext.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **ext)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    # USERNAMEobjects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email
