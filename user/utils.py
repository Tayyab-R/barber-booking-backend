from enum import Enum
import datetime

from django.utils import timezone

from . import models
class RolesChoices(Enum):
    BARBER = 'Barber'
    CUSTOMER = 'Customer'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    
def CreateSlots(barber):
    hours = 12
    today = datetime.datetime.today()
    for hour in range(hours):
        start_time = datetime.datetime(today.year, today.month, today.day, hour=hour, minute=0, tzinfo=timezone.timezone.utc)
        end_time = datetime.datetime(today.year, today.month, today.day, hour=hour+1, minute=0, tzinfo=timezone.timezone.utc)

        slot = models.Slots.objects.create(barber=barber, start_time=start_time, end_time=end_time)
        slot.save()
