from rest_framework import serializers

from . import models
from .utils import BookingStates
        
class DynamicFieldModelSerializer(serializers.ModelSerializer):
    """    
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                
                
class UserSerializer(DynamicFieldModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'password2', 'role']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            return serializers.ValidationError({'password' : 'passwords must match'})
        return attrs
    
    def create(self, validated_data):
        user =  models.CustomUser.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],                      
            email = validated_data['email'],
            phone_number = validated_data['phone_number']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = models.CustomUser
        fields = ['email', 'password']
        

class BarberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.BarberProfile
        fields = ['user', 'is_available']
        
    

class MinimalBarberSerializer(serializers.ModelSerializer):
    """
    Minimalistic Barber Serializer for users to see available barbers data
    with just email, phone_number
    """
    email = serializers.EmailField(source='user.email')  
    phone_number = serializers.CharField(source='user.phone_number')     
    # slots = serializers.DateTimeField(source='user.barber_profile.slots')    
    class Meta:
        model = models.CustomUser
        fields = ['id', 'email', 'phone_number']
        

class SlotSerializer(DynamicFieldModelSerializer):
    barber = MinimalBarberSerializer()
    class Meta:
        model = models.Slots
        fields = ['id', 'barber', 'start_time', 'end_time']
        
class ReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField()
    email = serializers.EmailField()
    class Meta:
        model = models.Review
        fields = ['review', 'email']
        
class MoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Money
        fields = ['amount']

    def __str__(self) -> str:
        return super().__str__()
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = ['reason']
    
