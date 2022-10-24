
from django.contrib import admin

from import_export.admin import ExportActionMixin
from import_export import resources

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import  Category, Post
from data.models import Log
from markdownx.admin import MarkdownxModelAdmin
from django.utils.translation import gettext_lazy as _


from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Category)


class LogResource(resources.ModelResource):

    class Meta:
        model = Log

class LogAdmin(ExportActionMixin, admin.ModelAdmin):
    
    list_filter = ('utm_1', 'utm_2', 'utm_3' , 'page', 'timestamp')
    resource_classes = [LogResource]

admin.site.register(Log, LogAdmin)

admin.site.register(Post,MarkdownxModelAdmin)