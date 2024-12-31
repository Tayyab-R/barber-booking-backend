from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from django.http import HttpRequest

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, BarberProfile, Slots, Review, Money, Booking

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'role', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields' : ('email', 'password', 'phone_number',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
        
    add_fieldsets = (
        (None,
         {
            'classes' : ('wide',),
            'fields' : (
                'email', 'password1', 'password2', 'phone_number', 
                'is_active', 'groups', 'user_permissions')}), 
        )
    
    ordering = ['email']
    
    
class BarberProfileAdmin(admin.ModelAdmin):
    model = BarberProfile
    list_display = ('user', 'is_available')
    search_fields = ('email', 'phone_number')
    
    
class SlotsAdmin(admin.ModelAdmin):
    model = Slots
    list_display = ('start_time', 'end_time')
    
class MoneyAdmin(admin.ModelAdmin):
    model = Money
    list_display = ('customer', 'amount', 'barber')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BarberProfile, BarberProfileAdmin)
admin.site.register(Slots, SlotsAdmin)
admin.site.register(Review)
admin.site.register(Money, MoneyAdmin)
admin.site.register(Booking)