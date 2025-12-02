from django.urls import path, include
from .views import *
urlpatterns = [
    path('', SignUpView.as_view(), name='sign-up'),
    path('login/', LogInView.as_view(), name='log-in'),
    path('logout/', LogOutView.as_view(), name='log-out'),
    
    path('otp/<str:type>/', GenerateOtpAPIView.as_view(), name='sign-up-email-verification'),
    path('reset/password/<str:type>/', ResetPasswordAPIView.as_view(), name='reset-password-verification'),
    path('reset/password/confirm/', ResetPasswordAPIView.as_view(), name='reset-password-')
]