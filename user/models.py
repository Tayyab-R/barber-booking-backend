from typing import Collection, Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from mysite import settings

from .manager import CustomUserManager

class CustomUser(AbstractUser):
    ROLES =(
        ('CUSTOMER', 'Customer'),
        ('BARBER', 'Barber'),
        ('ADMIN', 'Admin'),
    )

    username = None
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    role = models.CharField(max_length=50, choices=ROLES, default='CUSTOMER')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    
class BarberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='barber_profile')
    is_available = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.user.email
    
class Slots(models.Model):
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='slots')    
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    customer = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='slot')
    is_booked = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Start time: {self.start_time}. End time {self.end_time}'
    
    def clean(self, *args, **kwargs) -> None:
        if self.start_time >= self.end_time:
            raise ValidationError(
                'Start Time cannot come before or equal to End Time'
            )
            
        super(Slots, self).clean( )
        
    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super(Slots, self).save(*args, **kwargs)

    
class Review(models.Model):
    review = models.TextField()
    barber = models.ForeignKey(BarberProfile, related_name='reviews', on_delete=models.CASCADE)
    slot = models.ForeignKey(Slots, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)


class Money(models.Model):
    amount = models.PositiveIntegerField()
    barber = models.ForeignKey(BarberProfile, related_name='money', on_delete=models.CASCADE)
    barber_slot = models.ForeignKey(Slots, related_name='amount', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paid', on_delete=models.CASCADE)
    paid_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.amount)