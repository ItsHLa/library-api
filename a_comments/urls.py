from django.urls import path, include
from .views import *
urlpatterns = [
    # comments
    path('books/<str:book_pk>/comments/', CommentAPIView.as_view(), name='create - get'),
    path('books/<str:book_pk>/comments/<str:comment_pk>/', CommentAPIView.as_view(), name='update - delete'),
]