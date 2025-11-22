from django.contrib import admin

from a_books.models.book import Book
from a_books.models.book_author import BookAuthor
from a_books.models.book_category import BookCategory
from a_books.models.category import Category


admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookCategory)
admin.site.register(BookAuthor)