from django.db import models
from django.contrib.auth import get_user_model

from a_books.models.category_model import Category

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
    
    def add_categories(self, categories):
        categories = [
            BookCategory(book= self,category= category) for category in categories
            ]
        return BookCategory.objects.bulk_create(categories, ignore_conflicts=True)
    
    def remove_categories(self, categories):
        return self.categories.remove(*categories)
        
    def add_authors(self, authors):
        authors = [
            BookAuthor(book= self, author=author) for author in authors
        ]
        return BookAuthor.objects.bulk_create(authors, ignore_conflicts=True)
        
    def remove_authors(self, authors):
        self.authors.remove(*authors)
    
    def __str__(self) -> str:
        return f'{self.pk} - {self.title}'
    
class BookCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['book', 'category']

class BookAuthor(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['book', 'author']