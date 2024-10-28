from django.contrib import admin
from .models import Posts

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created", "updated"]
admin.site.register(Posts, PostAdmin)
