from enum import Enum
import datetime

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from . import models
class RolesChoices(Enum):
    BARBER = 'Barber'
    CUSTOMER = 'Customer'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
class BookingStates(Enum):
    ONGOING = 'OnGoing'
    COMPLETED = 'Completed'
    CANCELLED = 'CANCELLED'

    @classmethod
    def states(cls):
        return [(key.value, key.name) for key in cls]

    
def CreateSlots(barber):
    hours = 12
    today = datetime.datetime.today()
    for hour in range(hours):
        start_time = datetime.datetime(today.year, today.month, today.day, hour=hour, minute=0, tzinfo=timezone.timezone.utc)
        end_time = datetime.datetime(today.year, today.month, today.day, hour=hour+1, minute=0, tzinfo=timezone.timezone.utc)

        slot = models.Slots.objects.create(barber=barber, start_time=start_time, end_time=end_time)
        slot.save()

def get_slot_for_booking(slot):
    """
    Get slot from Booking model.
    """
    try:
        return models.Booking.objects.get(slot=slot)
    except ObjectDoesNotExist:
        return None
    
def get_barber_by_email(email):
    """
    Get barber from database by email
    """
    try:
        return models.BarberProfile.objects.get(user__email=email)
    except models.BarberProfile.DoesNotExist:
        return None