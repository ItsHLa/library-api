from typing import Any
from django.db import models
from a_books.models.book_author import BookAuthor
from a_books.models.book_category import BookCategory
from utils.search_service import SearchAndFilteration

class BookManager(models.Manager):
    
    def search(self, search, **kwargs):
        print(search)
        return SearchAndFilteration.search(
            manager= self,
            search_value= search,
            search_fields= ['title', 'description', 'categories__name', 'authors__first_name', 'authors__last_name'])
    
    def create(self, **kwargs: Any) -> Any:
        data = kwargs
        categories = data.pop('categories')
        authors = data.pop('authors')
        book = super().create(**data)
        self.add_categories(book, categories)
        self.add_authors(book, authors)
        return book
    
    def add_categories(self, book, categories):
        categories = [
            BookCategory(
                category= category,
                book= book
                ) for category in categories]
        return BookCategory.objects.bulk_create(categories)
    
    def remove_categories(self, book, categories, **kwargs: Any):
        book.categories.remove(*categories)
        return book
    
    def add_authors(self, book, authors):
        authors = [
            BookAuthor(
                author= author, 
                book= book) for author in authors
        ]
        return BookAuthor.objects.bulk_create(authors)
    
    def remove_authors(self, book, authors):
        book.authors.remove(*authors)
        return book