from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .permissions import AllowAny
from .serializers import *

class SignUpView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.check_user()
        user = serializer.save()
        serializer = SignUpSerializer(user, many=False)
        return Response(serializer.data, status=HTTP_201_CREATED)
        
class LogInView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        serializers = LoginSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        user = serializers.login()
        serializer = LoginSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

class LogOutView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializers = LogOutSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.logout()
        return Response(status=HTTP_200_OK)