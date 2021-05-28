from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manger for the UserProfile"""
    def create_user(self, first_name, last_name, email, password=None):
        """Create a new User Profile"""
        if not first_name:
            raise ValueError("First Name field is required")
        if not last_name:
            raise ValueError("Last Name field is required")
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """Creates a user with Admin privileges"""
        user = self.create_user(first_name, last_name, email, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database Schema for UserProfile"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        """This will return the full name of the user"""
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        """This will return only the user's first name"""
        return self.first_name

    def __str__(self):
        """This will return a string representation of the user"""
        return self.email

