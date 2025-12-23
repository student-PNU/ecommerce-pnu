from django.urls import path
from .views import CheckPhoneNumberView, UserCreationView, UserLoginView, UserLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register_step1/', CheckPhoneNumberView.as_view(), name='register_step1'),    
    path('register_step2/', UserCreationView.as_view(), name='register_step2'),
    path('Login/', UserLoginView.as_view(), name='Login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
]