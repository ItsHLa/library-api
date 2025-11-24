from rest_framework import serializers
from .models import *

class UserMixin:
    def get_user(self, obj):
        return {
            "id" : obj.user.id,
            "name" : f"{obj.user.first_name} {obj.user.last_name}"}

class ListCommentSerializer(UserMixin,serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.SerializerMethodField()
    replies_count = serializers.IntegerField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()

class CommentSerializer(UserMixin, serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    
    def get_reply_to(self, obj):
        print(obj.replies)
        return CommentSerializer(obj.replies, many=True, context=self.context).data
    


class CommentsRepresentationMixin:
    def to_representation(self, instance):
        return CommentSerializer(instance, context=self.context)

class CreateCommentSerializer(CommentsRepresentationMixin, serializers.Serializer):
    content = serializers.CharField()
    reply_to = serializers.IntegerField(required=False)
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

class UpdateCommentSerializer(CommentsRepresentationMixin, serializers.Serializer):
    content = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save(update_fields = ['content'])
        return instance
    
    
    
    