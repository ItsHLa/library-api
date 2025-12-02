
from datetime import datetime, timezone
from django.conf import settings
from a_users.utils.tokens import JwtTokens

class LinkGenerator:
    _SECRECT_KEY = settings.SECRET_KEY
    
    @classmethod
    def verify(cls, token):
        is_valid, data = JwtTokens.validate(
            token= token,
            secret_key= cls._SECRECT_KEY,
        )
        return is_valid, data
    
    @classmethod
    def generate(cls, email):
        # generate JWT 
        token = JwtTokens.create_token(
            payload={'email' : email},
            secret_key= cls._SECRECT_KEY,
            timedelta= settings.LINK_EXPARATION_TIMEDELTA
        )
        return f'http://127.0.0.1:8000/reset/password/confirm/{token}'