from django.urls import path, include

from a_books.views.book_views import *
from a_books.views.category_views import CategoryView



urlpatterns = [
    # categories
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<str:pk>/', CategoryView.as_view(), name='categories'),
        path('search/', BookSearchView.as_view(), name='book-search'),
    #book
    path('', BookView.as_view(), name='books'),
    path('<str:pk>/', BookView.as_view(), name='books'),
    
    
    path('<str:pk>/categories/', BookCategoryView.as_view(), name='books'),
    path('<str:pk>/authors/', BookAuthorsView.as_view(), name='books'),
    

    
]