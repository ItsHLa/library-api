from django.urls import path, include

from a_books.views.book_views import *
from a_books.views.category_views import CategoryView
from a_books.views.book_media_views import *


urlpatterns = [
    # categories
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<str:pk>/', CategoryView.as_view(), name='categories'),
    
   # book
    path('', BookView.as_view(), name='books'),
    path('<str:pk>/media/upload/<str:type>/', BookMediaAPIView.as_view(), name='books'),
    path('<str:public_id>/media/delete/<str:type>/', BookMediaAPIView.as_view(), name='books'),
    path('<str:pk>/', BookView.as_view(), name='books'),
    
    
    
    path('<str:pk>/categories/', BookCategoryView.as_view(), name='books'),
    path('<str:pk>/authors/', BookAuthorsView.as_view(), name='books'),
    

    
]