from rest_framework import serializers


from django.contrib.auth import get_user_model



User = get_user_model()

class AuthorSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.SerializerMethodField()
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class AuthorRepresentationMixin:
    def to_representation(self, instance):
        return AuthorSerializer(instance, context = self.context)
    
