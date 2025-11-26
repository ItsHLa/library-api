from django.db import models

from a_users.managers.blacklisted_token import BlacklistedTokensManager

class BlacklistedTokens(models.Model):
    token = models.TextField()
    jti = models.CharField(max_length=500)
    # created_at = models.DateTimeField()
    blacklisted_at = models.DateTimeField(auto_now=True)
    
    objects = BlacklistedTokensManager()