from django.contrib import admin
from .models import *
from .utils.blacklisted_tokens import BlacklistedTokens

admin.site.register(User)
admin.site.register(BlacklistedTokens)