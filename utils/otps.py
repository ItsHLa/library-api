import pyotp
from django.core.cache import cache


class OTP:
    _INTERVAL = 300
    
    # generate random key for OTP
    def _generate_key(self):
        secret  = pyotp.random_base32()
        return secret 
    
    # create OTP
    @classmethod
    def generate(cls, email):
        key = f'email:{email}'
        secret  = cls()._generate_key()
        totp = pyotp.TOTP(secret)
        otp = totp.now()
        cache.set(
            key,
            {'otp' : otp},
            timeout = cls._INTERVAL)
        print(totp.now())
        return otp
    
    # verify otp
    @classmethod
    def verify(cls, email, user_otp):
        key = f'email:{email}'
        data = cache.get(key)
        if not data:
            return False, 'OTP is expired'
        otp = data.get('otp', None)
        is_valid = otp == user_otp
        print(is_valid)
        if not is_valid:
            return False, 'OTP is not correct'
        cache.delete(key)
        return True, 'Success'
        