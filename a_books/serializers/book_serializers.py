from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404
from a_books.serializers.category_serializers import CategorySerializer
from a_books.serializers.author_serializer import *
from a_comments.serializers import CommentSerializer
from ..models import *

User = get_user_model()

class BookSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    categories = CategorySerializer(many=True)
    authors = AuthorSerializer(many=True)
    comments = serializers.SerializerMethodField()
    
    def get_comments(self, obj):
        return CommentSerializer(obj.book_comments, many=True).data

class BookListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    categories = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField()
    
    def get_categories(self, obj):
        return CategorySerializer(obj.categories, many=True).data

    def get_authors(self, obj):
        return AuthorSerializer(obj.authors, many=True).data

class BookRepresentationMixin:
    def to_representation(self, instance):
        return BookSerializer(instance, context=self.context).data
     
class CreateBookSerializer(BookRepresentationMixin, serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    categories = serializers.ListField(child=serializers.IntegerField())
    authors = serializers.ListField(child=serializers.IntegerField())
    
    def get_authors(self, authors):
        return get_list_or_404(User, pk__in = authors)
    
    def get_categories(self, categories):
        return get_list_or_404(Category, pk__in = categories)
    
    def create(self, validated_data):
        authors = validated_data.get('authors', None)
        validated_data['authors'] = self.get_authors(authors)
        
        categories = validated_data.get('categories', None)
        validated_data['categories'] = self.get_categories(categories)
        
        book = Book.objects.create(**validated_data)
        return book
       
class UpdateBookSerializer(BookRepresentationMixin, serializers.Serializer):
    title = serializers.CharField(required = False)
    description = serializers.CharField(required = False)
        
    def update(self, instance, validated_data): 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance

class UpdateBookCategoriesSerializer(BookRepresentationMixin, serializers.Serializer):
    categories = serializers.ListField(child=serializers.IntegerField(
    ))
    
    def add_categories(self):
        instance = Book.objects.add_categories(self.instance, self.validated_data['categories'])
        return instance
        
    def remove_categories(self):
        instance = Book.objects.remove_categories(self.instance, self.validated_data['categories'])
        return instance
    
class UpdateBookAuthorSerializer(BookRepresentationMixin, serializers.Serializer):
    authors = serializers.ListField(child=serializers.IntegerField())
    
    def add_authors(self):
        authors = get_list_or_404(User, pk__in = self.validated_data['authors'])
        instance = Book.objects.add_authors(self.instance, authors)
        return instance
        
    def remove_authors(self):
        authors = get_list_or_404(User, pk__in = self.validated_data['authors'])
        instance = Book.objects.remove_authors(self.instance, authors)
        return instance

