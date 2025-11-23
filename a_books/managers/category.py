from django.db import models
from utils.search_service import search

class CategoryQuerySet(models.QuerySet):
    
    def search(self, search_value):
        return search(
            self,
            search_value= search_value,
            search_fields= ['name'])

class CategoryManager(models.Manager):
    
    def get_queryset(self) -> models.QuerySet:
        return CategoryQuerySet(self.model, using=self.db)
    
    def search(self, search_value):
        return self.get_queryset().search(search_value)