from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from a_books.models.category_model import Category



User = get_user_model()

class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    
    

class CreateCategorySerializer(CategorySerializer):
    categories = serializers.ListField(
        write_only=True,
        min_length = 1,
        child=serializers.CharField(
             
        ))

    
    def check_categories_existence(self):
        query = Q()
        for name in self.validated_data['categories']:
            query |= Q(name__iexact = name)
        return Category.objects.filter(query)
    
    def create(self, validated_data):
        categories = [Category(name=data) for data in validated_data['categories']]
        return Category.objects.bulk_create(
            categories,
            )
    
class UpdateCategorySerializer(CategorySerializer):
    name = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
 