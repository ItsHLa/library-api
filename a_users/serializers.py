from rest_framework import serializers
from rest_framework.status import *
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
User = get_user_model()

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField( read_only = True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only = True,
        min_length = 8)

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField( read_only = True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only = True,
        min_length = 8)

class SignUpSerializer(UserSerializer):
    
    def check_user(self):    
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({
                'email' : ['User with this email already exists']})
        
        if User.objects.filter(username = self.validated_data["username"]).exists():
                        raise serializers.ValidationError({
                'username' : ['User with this username already exists']})
    
    def create(self, validated_data):
        return User.objects.create_user(**self.validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length = 8,
        write_only = True)  
    
    def verify_password(self):
        user = User.objects.get(email = self.validated_data['email'])
        if not user.check_password(self.validated_data['password']):
            raise serializers.ValidationError({'password' : ['No User account with this credintals']}, code=HTTP_404_NOT_FOUND) 
              
    def check_user(self):
        
        if not User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'email' : ['Users with this email dose not exists']}, code=HTTP_404_NOT_FOUND) 
    
    def login(self):
           self.check_user()
           self.verify_password()   
        
