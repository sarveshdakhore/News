from django.contrib import admin

# Register your models here.
from .models import Story, Bookmark

admin.site.register(Story)
admin.site.register(Bookmark)