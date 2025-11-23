from typing import Any
from django.db import models
from django.db.models import Q
from a_books.models.book_author import BookAuthor
from a_books.models.book_category import BookCategory
from utils.search_service import search

class BookQuerySet(models.QuerySet):
    
    def filter_by_category_ids(self, ids):
        query = Q()
        query |= Q(categories__id__in= ids)
        return self.filter(query)
    
    def filter_by_category_names(self, names):
        return self.filter(categories__name__in= names)
    
    def filter_by_author_ids(self, ids):
        return self.filter(authors__id__in= ids)
    
    def filter_by_author_names(self, names):
        query = Q()
        query |= Q(authors__first_name__in= names)
        query |= Q(authors__last_name__in= names)
        return self.filter(query)
    
    def search(self, search_value):
        return search(
            manager= self,
            search_value= search_value,
            search_fields= ['title', 'description', 'categories__name', 'authors__first_name', 'authors__last_name'])

class BookManager(models.Manager):
    
    def get_queryset(self) -> models.QuerySet:
        return BookQuerySet(self.model, using=self.db)
    
    def filter_by_category_names(self, names):
        return self.get_queryset().filter_by_category_names(names)
    
    def filter_by_category_ids(self, ids):
        return self.get_queryset().filter_by_category_ids(ids)
    
    def filter_by_author_names(self, names):
        return self.get_queryset().filter_by_author_names(names)
    
    def filter_by_author_ids(self, ids):
        return self.get_queryset().filter_by_author_ids(ids)
    
    def search(self, search_value, **kwargs):
        return self.get_queryset().search(search_value)
    
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