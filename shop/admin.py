from django.contrib import admin
from .models import Category, Product

from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib.auth.models import Permission

# from django.contrib import admin
# from django.contrib.auth.models import Group
#
# admin.site.unregister(Group)

# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import GroupAdmin
#
# class MyUserAdmin(UserAdmin):
#
#     def get_form(self, request, obj=None, **kwargs):
#         # Get form from original UserAdmin.
#         form = super(MyUserAdmin, self).get_form(request, obj, **kwargs)
#         if 'user_permissions' in form.base_fields:
#             permissions = form.base_fields['user_permissions']
#             # permissions.queryset = permissions.queryset.filter(content_type='log entry')
#             #permissions.queryset = permissions.queryset.exclude(content_type__app_label__in=['admin', 'auth'])
#         return form
#
#
#
#
#
# admin.site.unregister(User)  # You must unregister first
# admin.site.register(User, MyUserAdmin)
#
#
# class MyGroupAdmin(GroupAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         # Get form from original UserAdmin.
#         form = super(MyGroupAdmin, self).get_form(request, obj, **kwargs)
#         if 'permissions' in form.base_fields:
#             permissions = form.base_fields['permissions']
#             permissions.queryset = permissions.queryset.filter(content_type__name='log entry')
#
#         return form
#
#
# admin.site.unregister(Group)  # You must unregister first
# admin.site.register(Group, MyGroupAdmin)


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
