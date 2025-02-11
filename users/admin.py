from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Users, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'users'


class UsersInline(admin.StackedInline):
    model = Users
    can_delete = False
    verbose_name_plural = 'Users Info'


class UserAdmin(BaseUserAdmin):
    inlines = (UsersInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_title')
    list_select_related = ('users', 'users__profile')

    def get_profile_title(self, instance):
        return instance.users.profile.title if instance.users.profile else ''

    get_profile_title.short_description = 'Title'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
