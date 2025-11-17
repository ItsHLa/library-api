from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404
from a_books.serializers.category_serializers import CategorySerializer
from a_books.serializers.author_serializer import *
from ..models import *

User = get_user_model()

class BookSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    categories = CategorySerializer(many=True)
    authors = AuthorSerializer(many=True)
    
    def get_authors(self, obj):
        authors = obj.authors.all()
        return [f"{author.first_name} {author.last_name}" for author in authors]
    
class CreateBookSerializer(BookSerializer):
    categories = serializers.ListField(child=serializers.IntegerField())
    authors = serializers.ListField(child=serializers.IntegerField())
    
    
    def get_authors(self, authors):
        return get_list_or_404(User, pk__in = authors)
    
    def get_categories(self, categories):
        return get_list_or_404(Category, pk__in = categories)
    
    def create(self, validated_data):
        authors = self.validated_data.pop('authors', None)
        authors = self.get_authors(authors)
        
        categories = self.validated_data.pop('categories', None)
        categories = self.get_categories(categories)
        book = Book.objects.create(**self.validated_data,)
        book.add_categories(categories)
        book.add_authors(authors)
        return book
       
class UpdateBookSerializer(BookSerializer):
    title = serializers.CharField(required = False)
    description = serializers.CharField(required = False)
    categories = serializers.ListField(child=serializers.IntegerField(), required = False)
    authors = serializers.ListField(child=serializers.IntegerField(), required = False)
        
    def update(self, instance, validated_data): 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance

class UpdateBookCategoriesSerializer(serializers.Serializer):
    categories = serializers.ListField(child=serializers.IntegerField())
    
    def add_categories(self):
        categories = get_list_or_404(Category, pk__in= self.validated_data['categories'])
        self.instance.add_categories(categories)
        
    def remove_categories(self):
        categories = get_list_or_404(Category, pk__in= self.validated_data['categories'])
        self.instance.remove_categories(categories)

