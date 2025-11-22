from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save, m2m_changed
from django.db.models import Count

from a_books.models.book import Book
from a_books.models.category import Category

@receiver(m2m_changed, sender=Book.categories.through)
def handle_category_removal(sender, instance, action, reverse, **kwargs):
    if reverse:
        books = Book.objects.annotate(
            count = Count('categories')
        ).filter(
            categories=instance,
            count = 1)
        
        books.delete()
    if not reverse:
        if instance.categories.count() == 0:
            instance.delete()        

@receiver(pre_delete, sender=Category)
def handle_category_deletion(sender, instance, **kwargs):
    books = Book.objects.annotate(
            category_count = Count('categories')).filter(
               categories = instance,
                category_count=1)
    books.delete()

