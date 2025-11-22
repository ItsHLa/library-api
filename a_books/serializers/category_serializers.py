from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from a_books.models.category import Category

User = get_user_model()

class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)

class CategoryMixin:
    def to_representation(self, instance):
        return CategorySerializer(instance=instance, context = self.context).data
    
class CreateCategorySerializer(CategoryMixin, serializers.Serializer):
    name= serializers.CharField()
    
    def check_category_existence(self):
        return Category.objects.filter(name = self.validated_data['name']).exists()
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
class UpdateCategorySerializer(CategoryMixin, serializers.Serializer):
    name = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
 