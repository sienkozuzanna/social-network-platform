from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Post, Profile, Follow, Like, Comment

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'profile'

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

    def delete_model(self, request, obj):
        try:
            profile = Profile.objects.get(user=obj)
            profile.delete()
        except Profile.DoesNotExist:
            pass
        super().delete_model(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
