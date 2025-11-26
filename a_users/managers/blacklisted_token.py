from django.db import models

class BlacklistedTokensManager(models.Manager):
    
    def blacklist(self, token, jti):
        return self.create(
            token= token,
            jti= jti)
    
    def is_blacklisted(self, jti):
        return self.filter(jti=jti).exists()