
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BookAuthor(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['book', 'author']