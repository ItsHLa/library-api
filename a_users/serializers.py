from rest_framework import serializers
from rest_framework.status import *
from django.contrib.auth import get_user_model

from a_users.utils.refresh_tokens import RefreshToken


User = get_user_model()

class GenerateOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

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
    token = serializers.SerializerMethodField()
    is_admin = serializers.BooleanField(required= False)
    
    def check_user(self):    
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({
                'email' : ['User with this email already exists']})
        
        if User.objects.filter(username = self.validated_data["username"]).exists():
                        raise serializers.ValidationError({
                'username' : ['User with this username already exists']})
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return {
            'refresh' : token.refresh,
            'access' : token.access}
    
    def create(self, validated_data):
        return User.objects.create_user(**self.validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only = True)
    password = serializers.CharField(
        min_length = 8,
        write_only = True)  
    token = serializers.SerializerMethodField()
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return {
            'refresh' : token.refresh,
            'access' : token.access}
    
    def verify_password(self, user):
        if not user.check_password(self.validated_data['password']):
            raise serializers.ValidationError({'password' : ['No User account with this credintals']}, code=HTTP_404_NOT_FOUND)
              
    def check_user(self):
        try:
            user = User.objects.get(email = self.validated_data['email'])
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError({'email' : ['Users with this email dose not exists']}, code=HTTP_404_NOT_FOUND) 

            
        
    
    def login(self):
           user = self.check_user()
           self.verify_password(user)  
           return user 
        
class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        write_only = True)
    
    def logout(self):
           RefreshToken.blacklist(self.validated_data['refresh'])
        
