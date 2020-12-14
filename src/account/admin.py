from account.models import Avatar, User

from django.contrib import admin


class AvatarInline(admin.TabularInline):
    model = Avatar
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = (AvatarInline, )

    list_display = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']

    list_filter = ['is_staff', 'is_active', 'is_superuser']

    readonly_fields = ('password', 'first_name', 'last_name', 'is_active', 'groups', 'user_permissions')

    search_fields = ('id', 'email')

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('account.full_edit') \
                or request.user.is_superuser:
            return ()
        return super().get_readonly_fields(request, obj=obj)


class AvatarAdmin(admin.ModelAdmin):
    raw_id_fields = [('user'), ]
    # readonly_fields = ('user', )


admin.site.register(User, UserAdmin)
admin.site.register(Avatar, AvatarAdmin)
