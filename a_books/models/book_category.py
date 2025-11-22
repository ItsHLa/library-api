from django.db import models


class BookCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['book', 'category']

