from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from .permissions import  IsShopOwner, IsBarber
from . import serializers
from .models import CustomUser, BarberProfile, Slots, Review, Money

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def RetrieveUpdateDeleteUser(request, pk=None):
    print(request.user)
    try:
        user = get_object_or_404(CustomUser, pk=pk) if pk else None
        
        if request.method == 'GET':
            if pk:
                serializer = serializers.UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            user = CustomUser.objects.all()
            serializer = serializers.UserSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            user = CustomUser.objects.get(pk=pk)
            serializer = serializers.UserSerializer(user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'Success' : 'User updated successfully'}, status=status.HTTP_202_ACCEPTED)

            return Response({'Message' : 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'DELETE':
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response({'Message' : 'User deleted.'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'Error' : ' User not found'}, status=status.HTTP_404_NOT_FOUND)
    

@swagger_auto_schema(request_body=serializers.RegisterUserSerializer, method='post')
@api_view(['POST'])
def RegisterUser(request):
    """
    POST /api/register/
    - Purpose:
        Signup a new user by providing first name, last name, email, and password.

    - Request Parameters:
        - first_name (string) : user's first name
        - last_name (string) :  user's last_name
        - email (string) : user's email
        - password (string) : user's password
        - password2 (string) : user's password again for confirmation
        - phone_number - optional (string) : user's phone_number
    
    - Respones: 
        - 201 Created : Returns registered user's email
        - 400 Bad Request: Validation errors or password mismatch
    """
    if request.method == 'POST':
        user = request.data
        serializer = serializers.RegisterUserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Registered': serializer.data['email']}, status=status.HTTP_201_CREATED)
        
@authentication_classes([TokenAuthentication])
@swagger_auto_schema(request_body=serializers.LoginUserSerializer, method='post')        
@api_view(['POST'])
def LoginView(request):
    """
    
    POST /api/login/
    - Purpose
        Login a user with provided email and password
        
    - requires:
        - email (string)
        - password (string)

    - Returns
        - 200 OK: With a session token
        - 401 Unauthorized: Invalid email or password
        
    """
    if request.method == 'POST':
        data = request.data
        serializer = serializers.LoginUserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    token.delete()
                    token = Token.objects.create(user=user)
                return Response({'Token' : token.key}, status=status.HTTP_200_OK)

            return Response({'Message' : 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    """
    POST /api/logout/
    - Purpose:
        Logout user.
    
    - Request Parameters:
        - No Parameters

    - Returns:
        - 200 OK: Successfully logged out.
    """
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'Message' : 'Successfuly logged out.'}, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsShopOwner])
def ListRetrieveDeleteUpdateBarber(request, pk=None):
    """
    POST /api/barbers/
    - Purpose:
        A shop owner can see barbers data working in his shop. 
        Moreover, shop owner can Delete barbers data if needed.
    
    - Request Parameters:
        
        
    - Returns:
        - 200 OK: Barbers data
        - 404 Not Found : No Barbers found
    """
    
    try:
        user = get_object_or_404(BarberProfile, pk=pk) if pk else None
        if request.method == 'GET':
            if pk:
                serializer = serializers.BarberSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            user = BarberProfile.objects.filter(owner=request.user.owner_profile)
            serializer = serializers.BarberSerializer(user, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            user = BarberProfile.objects.get(pk=pk)
            user.delete()
            return Response({'Message' : 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except:
          return Response({'Message' : 'User Not found'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(request_body=serializers.BarberSerializer, method='post')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateBarberProfile(request):
    """
    POST /api/barber/signup
    
    - Purpose:
        - User convert to Barber role
    
    - Required Parameters:
        - Barber needs 'available_at' and 'is_available' parameters but can be done later in profile
        - Needs to be login already
    
    - Returns:
        400 Bad Request: Barber profile already exists
        201 Created: Barber Profile created
    """
    user = request.user
    if hasattr(user, 'barber_profile'):
        return Response({'Message': 'Profile Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
        
    user.role = 'BARBER'
    user.save()
    barber = BarberProfile.objects.create(user=user)
    barber.save()

    return Response({'Message' : 'Barber Profile Created.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Profile(request):
    """
    POST /api/profile/
    
    - Purpose:
        - A user can see his profile if he is already logged in. 
    
    - Required Paremeters:
        - Needs to be logged in first
        - No parameters required
    
    - Returns:
        200 OK : User profile 
     
    """
    user = request.user
    profile = CustomUser.objects.get(pk=user.id)
    serializer = serializers.UserSerializer(profile)
    return Response({'User Profile': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsBarber])
def SlotCreationForBarberView(request):
    """
    POST /api/barber/create-slot
    
    - Purpose:
        - Make barber able to create his time slot on which he is avialable
    
    - Parameters Requirements:
        - already logged in
    """
    if request.method == 'POST':
        data = request.data
        
        serializer = serializers.SlotSerializer(data=data, fields=('start_time', 'end_time'))
        serializer.is_valid(raise_exception=True)
        
        barber = BarberProfile.objects.get(user=request.user)
        barber.is_available = True
        
        slot = Slots.objects.create(barber=barber, start_time=serializer.validated_data['start_time'], end_time=serializer.validated_data['end_time'])
        slot.save()
        return Response({'Message' : 'Time slot created successfuly'}, status=status.HTTP_201_CREATED)

    
@api_view(['GET'])
def ListBarberSlots(request):
    if request.method == 'GET':
        slots = Slots.objects.filter(is_booked=False)
        serializer = serializers.SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def BookBarberSlot(request, pk):
    if request.method == 'POST':
        customer = request.user
        try:
            
            booking_slot = Slots.objects.get(pk=pk)
            if booking_slot.is_booked == True:

                return Response({'Cannot book slot' : 'Slot already booked'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'Message' : 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)
        booking_slot.is_booked = True
        booking_slot.customer = customer
        booking_slot.save()
        return Response({'Message' : 'Booking slot created.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def WriteReviewOfBarberView(request, pk):
    serializer = serializers.ReviewSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    customer = request.user
    barber_email = serializer.validated_data['email']
    try:
        slot = Slots.objects.filter(barber__isnull=False).get(pk=pk)
        print(slot)
        barber = slot.barber
    except:
        return Response({'Error' : 'Slot or Barber does not exist'}, status=status.HTTP_404_NOT_FOUND)    
        
    review = Review.objects.create(barber=barber, customer=customer,slot=slot, review=serializer.validated_data['review'])
    review.save()

    return Response({'Status' : 'Success', 'Message' : 'Review created.'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def PayMoneyToBarberView(request, pk):
    if request.method == 'POST':
        serializer = serializers.MoneySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:    
            slot_being_paid = Slots.objects.filter(barber__isnull=False).get(pk=pk)
            barber = slot_being_paid.barber
            paying_customer = request.user
            slot_customer = slot_being_paid.customer
            
        except:
            return Response({'Error' : 'Slot Not Found!!!'}, status=status.HTTP_404_NOT_FOUND)
   
        if paying_customer == slot_customer:
            amount = Money.objects.create(barber_slot=slot_being_paid, amount=serializer.validated_data['amount'], barber=barber, customer=paying_customer, )
            amount.save()
            return Response(
                {'Message' : 'Payment Successfull',
                'Amount' : serializer.validated_data['amount'],
                'Paid by' : paying_customer.email,
                'Paid To' : barber.user.email}, status=status.HTTP_201_CREATED)
        return Response({'Error' : 'Unauthorized Payment!!'}, status=status.HTTP_403_FORBIDDEN)        
    