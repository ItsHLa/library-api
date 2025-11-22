from django.db import models
from django.contrib.auth import get_user_model

from a_books.managers.book import BookManager
from a_books.models.category import Category

User = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    categories = models.ManyToManyField(
        Category,
        through= 'BookCategory',
        through_fields=['book','category'],
        related_name='books')
    authors = models.ManyToManyField(
        User,
        through= 'BookAuthor',
        through_fields=['book', 'author'],
        related_name='authored_books')
    
    objects = BookManager()
    
    def __str__(self) -> str:
        return f'{self.pk} - {self.title}'
    



