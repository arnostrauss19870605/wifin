
from django.contrib import admin

from import_export.admin import ExportActionMixin,ImportExportModelAdmin
from import_export import resources

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import  Category, Post, Topic, Comment,Registered_User,Country,Domain,Domain_User
from vouchers.models import Voucher,Location,Activation,VoucherType
from data.models import Log
from markdownx.admin import MarkdownxModelAdmin
from django.utils.translation import gettext_lazy as _


from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password','site')}),
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
admin.site.register(VoucherType)
admin.site.register(Activation)
admin.site.register(Location)


class LogResource(resources.ModelResource):

    class Meta:
        model = Log

class VoucherResource(resources.ModelResource):

    class Meta:
        model = Voucher

class LogAdmin(ExportActionMixin, admin.ModelAdmin):
    
    list_filter = ( 'utm_1', 'utm_2', 'utm_3' , 'page', 'timestamp')
    resource_classes = [LogResource]

class VoucherAdmin(ExportActionMixin, admin.ModelAdmin):
       
    list_filter = ('company_name', 'voucher_type', 'sell_price' , 'card_code', 'language', 'hs_domian_data_id')
    resource_classes = [VoucherResource]

admin.site.register(Log, LogAdmin)


admin.site.register(Post,MarkdownxModelAdmin)


@admin.register(Voucher)
class PersonAdmin(ImportExportModelAdmin):
    
    pass

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug':('title',)}
    raw_if_fields = ('author')
    date_hierarchy = ('publish')
    ordering = ('status','publish')
  

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'topic', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Registered_User)
class Registered_UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('hsDomainsDataID','hsUsersID','username','first_name','last_name','email','date_imported','uploaded','date_uploaded')
    list_filter = ('uploaded','date_imported','reseller_name','manager_name','product')
    date_hierarchy = ('date_imported')

@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('id', 'country_code', 'country_name')
    search_fields = ('id', 'country_code', 'country_name')

@admin.register(Domain)
class DomainAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('id', 'description', 'domain_id','last_extracted_date','date_created','last_updated')

@admin.register(Domain_User)
class DomainUserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=('user_id', 'domain_id','last_extracted_date','date_created','last_updated','extracted')
    search_fields = ('user_id', 'domain_id')
    list_filter = ('last_updated','date_created','last_extracted_date','domain_id','extracted')

   