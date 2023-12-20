from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Post, Comment

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    def get_likes_count(self, obj):
        return obj.like_set.filter(is_like=True).count()

    get_likes_count.short_description = 'Likes Count'

    def comment_count(self, obj):
        return obj.comment_set.count()

    list_display = ['title', 'author', 'created_at', 'get_likes_count', 'comment_count']
    readonly_fields = ['get_likes_count', 'comment_count']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
