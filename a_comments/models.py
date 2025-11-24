from django.db import models
from django.contrib.auth import get_user_model
from a_books.models.book import Book

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    book = models.ForeignKey(Book,related_name='book_comments', on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='replies', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def replies_count(self):
        return self.replies.count()
    
    def __str__(self):
        return f"{self.pk} - {self.content}"
