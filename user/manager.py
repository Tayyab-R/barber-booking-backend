from django.contrib.auth.base_user import BaseUserManager
from .utils import RolesChoices

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            return ValueError('Email must be set.')

        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save superuser
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = RolesChoices.ADMIN.value

        if extra_fields.get('is_staff') != True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') != True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

        