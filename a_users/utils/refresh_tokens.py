import jwt
import json
from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class RefreshToken:
    _SECRET_KEY  = settings.SECRET_KEY
    refresh = None
    access = None
    
    def _create_token(self, payload, timedelta):
        token_payload = {
            **payload,
            'exp' : datetime.now(timezone.utc) + timedelta
           
        }
        return jwt.encode(
           token_payload,
            self._SECRET_KEY,
            algorithm='HS256')
    
    @classmethod
    def for_user(cls, user):
        payload = {
           'id' : user.id,
           'email' : user.email
        }
        print(payload)
        token = RefreshToken()
        token.refresh = token._create_token(payload, settings.REFRESH_EXPARATION_TIMEDELTA)
        token.access = token._create_token(payload, settings.ACCESS_EXPARATION_TIMEDELTA)
        return token
    
    @classmethod
    def validate(cls, token):
        try:
            payload = jwt.decode(token,cls._SECRET_KEY,algorithms=['HS256'])
            exparation = payload.pop('exp')
            return True, payload
        except jwt.ExpiredSignatureError:
            return False,'Token has expired'
        except jwt.InvalidTokenError:
            return False,'Invalid Token'
        
    
# user_data = {'user_id': 123, 'email': 'john_doe@gmail.com'}
# token = RefreshToken.for_user(user_data)
# print(f"Generated R-Token: {token.refresh}")
# print(f"Generated A-Token: {token.access}")

# user_data = {'user_id': 123, 'email': 'john_doe@gmail.com'}
# res = JWTTokens.validate(token)
# print(f"Payload: {res}")
