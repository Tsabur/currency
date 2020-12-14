from django.contrib import admin

from rate.models import Rate


class RateAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'source', 'buy', 'sale', 'created', ]

    list_filter = ['currency', 'source', 'created', ]

    actions = None

    def has_delete_permission(self, request, obj=None):
        return False

    readonly_fields = ('currency', 'source',)

    def get_readonly_fields(self, request, obj=None):
        # if request.user.is_superuser:
        # if request.user.groups.filter(name='Super Manager').exists() \   <---- WRONG!!!
        if request.user.has_perm('rate.full_edit') \
                or request.user.is_superuser:
            return ()
        return super().get_readonly_fields(request, obj=obj)


admin.site.register(Rate, RateAdmin)
