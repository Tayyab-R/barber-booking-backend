from django.urls import path
 
from . import views

urlpatterns = [
    path('users/', views.RetrieveUpdateDeleteUser),
    path('user/<int:pk>/', views.RetrieveUpdateDeleteUser),
    path('register/', views.RegisterUser),
    path('login/', views.LoginView),
    path('logout/', views.LogoutView),
    path('barbers/', views.ListRetrieveDeleteUpdateBarber),
    path('barbers/<int:pk>/', views.ListRetrieveDeleteUpdateBarber),
    path('barber/signup/', views.CreateBarberProfile),
    path('profile/', views.Profile),
    path('barber/slots/', views.ListBarberSlots),
    path('barber/slots/<int:pk>/', views.BookBarberSlot),
    path('barber/write-review/<int:pk>/', views.WriteReviewOfBarberView),
    path('barber/pay/<int:pk>/', views.PayMoneyToBarberView),

]