from django.db import models
from django.contrib.auth import get_user_model

from a_books.managers.category import CategoryManager

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    objects = CategoryManager()
    
    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"
    

