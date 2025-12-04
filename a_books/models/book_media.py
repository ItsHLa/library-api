from django.db import models

from a_books.models.book import Book


class BookMedia(models.Model):
    book = models.ForeignKey(Book, related_name='media', on_delete=models.CASCADE)
    public_id = models.CharField(max_length=500)
    resource_type = models.CharField(max_length=100)
    bytes = models.IntegerField()
    secure_url = models.URLField()
    display_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f'{self.pk} | {self.public_id} | {self.book.pk} | {self.bytes}'