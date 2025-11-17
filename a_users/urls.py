from django.urls import path, include
from .views import *
urlpatterns = [
    path('', SignUpView.as_view(), name='sign-up'),
    path('login/', LogInView.as_view(), name='log-in')
]