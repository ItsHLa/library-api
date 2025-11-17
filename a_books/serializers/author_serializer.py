from rest_framework import serializers
from django.shortcuts import get_list_or_404

from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.SerializerMethodField()
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
class UpdateBookAuthorSerializer(serializers.Serializer):
    authors = serializers.ListField(child=serializers.IntegerField())
    
    def add_authors(self):
        authors = get_list_or_404(User, pk__in = self.validated_data['authors'])
        self.instance.add_authors(authors)
        
    def remove_authors(self):
        authors = get_list_or_404(User, pk__in = self.validated_data['authors'])
        self.instance.remove_authors(authors)