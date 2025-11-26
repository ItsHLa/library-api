from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import get_user_model

from a_users.utils.blacklisted_tokens import BlacklistedTokens
from a_users.utils.refresh_tokens import RefreshToken

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if header and header.startswith('Bearer'):
            token = header.split(' ')[1]
            valid, data = RefreshToken.validate(token)
            # check if blacklisted
            if BlacklistedTokens.objects.is_blacklisted(data['jti']):
                raise AuthenticationFailed("Token is blacklisted")
            
            if not valid:
                raise AuthenticationFailed(data)
            try:
                user = User.objects.get(id=data['id'])
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')
            return user, token
        return
            
        