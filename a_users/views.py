from utils.email_service import EmailService
from utils.link_generator import LinkGenerator
from utils.otps import OTP
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .permissions import AllowAny
from .serializers import *

class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    
    def _generate(self, request):
        serializer = ResetPasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        ## generate link
        link = LinkGenerator.generate(email)
        print(link)
        
        try:
            ## send email
            EmailService.send(
            subject = 'Email Verification',
            message =  f'Your verification link is {link} \n It expiers after 15 minutes',
            from_mail ='resqteambackup@gmail.com',
            to_mails_list= [email])
            return 'Verification link sent successfully', HTTP_200_OK
        except Exception as e :
            return 'Failed to send verification link. Please try again later.', HTTP_400_BAD_REQUEST
    
    def _verify(self, request) : 
        data = request.data
        serializer = ConfirmResetPasswordSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']  
        password = serializer.validated_data['password']  
        is_valid, data = LinkGenerator.verify(token)
        print(data)
        if is_valid:
            try:
                user = User.objects.get(email= data['email'])
                user.set_password(password)
                return 'Password reset successfully', HTTP_200_OK
            except User.DoesNotExist:
                return 'User with this email dose not exsists', HTTP_400_BAD_REQUEST
        else:
            return 'Verification Link is expired', HTTP_400_BAD_REQUEST 
         
    def post(self, request, type= None,   *args, **kwargs):
        if type == 'generate':
           msg, status =  self._generate(request)
        else:
           msg, status = self._verify(request)
        return Response({'detail' : msg}, status = status)



class GenerateOtpAPIView(APIView):
    permission_classes = [AllowAny]
    
    def _generate(self, request):
        serializer = GenerateOtpSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        ## generate otp
        code = OTP.generate(email)
        
        try:
            ## send email
            EmailService.send(
            subject = 'Email Verification',
            message =  f'Your verification code is {code}',
            from_mail ='resqteambackup@gmail.com',
            to_mails_list= [email])
            return 'OTP sent successfully', HTTP_200_OK
        except Exception as e :
            return 'Failed to send OTP. Please try again later.', HTTP_400_BAD_REQUEST
    
    def _verify(self, request) : 
        data = request.data
        serializer = VerifyOtpSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']  
        otp = serializer.validated_data['otp']  
        is_valid, msg = OTP.verify(email, otp)
        if is_valid:
            return msg, HTTP_200_OK
        return msg, HTTP_400_BAD_REQUEST 
         
    def post(self, request, type, *args, **kwargs):
        if type == 'generate':
           msg, status =  self._generate(request)
        if type == 'verify':
            msg, status = self._verify(request)
        return Response({'detail' : msg}, status = status)



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