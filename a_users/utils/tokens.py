from uuid import uuid4
import jwt
import json
from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model
from django.conf import settings

from a_users.utils.blacklisted_tokens import BlacklistedTokens

User = get_user_model()

class JwtTokens:
    
    @staticmethod
    def create_token(payload, timedelta, secret_key):
        token_payload = {
            **payload,
            'exp' : datetime.now(timezone.utc) + timedelta,}
        return jwt.encode(
           token_payload,
            secret_key,
            algorithm='HS256')
    
    @staticmethod
    def validate(token, secret_key):
        try:
            payload = jwt.decode(token,secret_key,algorithms=['HS256'])
            exparation = payload.pop('exp')
            return True, payload
        except jwt.ExpiredSignatureError:
            return False,'Token has expired'
        except jwt.InvalidTokenError:
            return False,'Invalid Token'
    

class RefreshToken:
    _SECRET_KEY  = settings.SECRET_KEY
    refresh = None
    access = None
    
    @classmethod
    def blacklist(cls, refresh):
        valid, data = RefreshToken.validate(refresh)
        
        access_payload = {
            'id':data['id'],
            'a_jti': data['a_jti']}

        access = cls()._create_token(access_payload, settings.ACCESS_EXPARATION_TIMEDELTA)
        
        BlacklistedTokens.objects.blacklist(
            token = refresh,
            jti = data['jti'])
        BlacklistedTokens.objects.blacklist(
            token = access,
            jti = data['a_jti'])
        
    def _create_token(self, payload, timedelta):
        token = JwtTokens.create_token(
            payload,
            timedelta,
            self._SECRET_KEY,)
        return token
    
    def _set_jti(self):
        return uuid4().hex  
    
    def _create_access(self, payload):
        jti = self._set_jti()
        payload['jti'] = jti
        access = self._create_token(payload, settings.ACCESS_EXPARATION_TIMEDELTA)
        return access, jti
    
    def _create_refresh(self, payload, a_jti):
        jti = self._set_jti()
        payload['jti'] = jti
        payload['a_jti'] = a_jti
        refresh = self._create_token(payload, settings.REFRESH_EXPARATION_TIMEDELTA)
        return refresh
    
    @classmethod
    def for_user(cls, user):
        payload = {'id' : user.id}
        token = RefreshToken()
        
        token.access, a_jti =  token._create_access(payload)
        token.refresh = token._create_refresh(payload, a_jti)
        
        return token
    
    @classmethod
    def validate(cls, token):
        return JwtTokens.validate(token, cls._SECRET_KEY)
        
