from django.contrib import admin
from .models import Accounts, Posts, Chats

# Register your models here.

admin.site.register(Accounts)
admin.site.register(Posts)
admin.site.register(Chats)
