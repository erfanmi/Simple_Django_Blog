from django.contrib import admin
from .models import Post


# Register your models here.
# registering models here makes it possible for us to manage models from admin GUI
# list display is used here to determine what should be shown in admin panel for our model

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'datetime_modified')
    ordering = ('status',)

# admin.site.register(Post, PostAdmin)
