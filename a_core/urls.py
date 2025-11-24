from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('a_users.urls')),
    path('api/books/', include('a_books.urls')),
    path('api/', include('a_comments.urls')),
]
