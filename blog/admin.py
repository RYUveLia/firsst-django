from django.contrib import admin
from .models import Post, Game

admin.site.register(Game)
admin.site.register(Post)