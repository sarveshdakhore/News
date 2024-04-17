from django.contrib import admin

# Register your models here.
from .models import Story, Bookmark, ApiKey, UserProfile

admin.site.register(Story)
admin.site.register(Bookmark)
admin.site.register(ApiKey)
admin.site.register(UserProfile)