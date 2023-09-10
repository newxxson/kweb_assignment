from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        if not id:
            raise ValueError("The id field must be set")
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        user = self.create_user(id, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=15, unique=True)
    ROLE_CHOICES = (
        ("student", "Student"),
        ("professor", "Professor"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["name", "student_id", "role"]

    def __str__(self):
        return self.id
