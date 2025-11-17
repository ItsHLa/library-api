from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .serializers import *

class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.check_user()
        user = serializer.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=HTTP_201_CREATED)
        
class LogInView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializers = LoginSerializer(data=data)
        serializers.is_valid(raise_exception=True)
        serializers.login()
        return Response(status=HTTP_200_OK)