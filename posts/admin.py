from django.contrib import admin
from .models import Likes, Comments, Posts
# Register your models here.
admin.site.register([Likes,Comments, Posts])
