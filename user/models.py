from typing import Collection, Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from mysite import settings

from .manager import CustomUserManager
from .utils import RolesChoices, BookingStates


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, TimeStampModel):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    role = models.CharField(max_length=50, choices=RolesChoices.choices, default=RolesChoices.CUSTOMER.value)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

def __str__(self) -> str:
    return self.email

    
class BarberProfile(TimeStampModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='barber_profile')
    is_available = models.BooleanField(default=False)
        
    def __str__(self) -> str:
        return self.user.email
    
class Slots(TimeStampModel):  
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    barber = models.ForeignKey(BarberProfile, on_delete=models.CASCADE, related_name='slots')
    
class Booking(TimeStampModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    slot = models.OneToOneField(Slots, on_delete=models.CASCADE, related_name='bookings')    
    state = models.CharField(max_length=15, choices=BookingStates.states, default=BookingStates.ONGOING.value)
    reason = models.TextField(blank=True, null=True)

class Review(TimeStampModel):
    review = models.TextField()
    barber = models.ForeignKey(BarberProfile, related_name='reviews', on_delete=models.CASCADE)
    slot = models.ForeignKey(Slots, related_name='reviews', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', null=True, on_delete=models.SET_NULL)


class Money(TimeStampModel):
    amount = models.PositiveIntegerField()
    barber = models.ForeignKey(BarberProfile, related_name='money', on_delete=models.CASCADE)
    barber_slot = models.ForeignKey(Slots, related_name='amount', on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='paid', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.amount)