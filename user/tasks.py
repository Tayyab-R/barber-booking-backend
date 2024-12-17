# from celery import shared_task

# from .models import BarberProfile, Slots
# from django.utils import timezone

# @shared_task
# def CheckSlotTime():
#     slots = Slots.objects.all()
#     current_time = timezone.now()

#     barbers = BarberProfile.objects.filter(is_available=True)

#     for slot in slots:
#         if current_time > slot.end_time:
#             print('Time is over. Setting slots to None')
#             slot.start_time = None
#             slot.end_time = None
#             slot.customer = None
#             slot.save()

#         else:
#             print('Time is not over')