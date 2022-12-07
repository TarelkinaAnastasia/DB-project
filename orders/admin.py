from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete = False
    raw_id_fields = ['product']
    readonly_fields = ('product', 'price', 'quantity')


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    readonly_fields = ('id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city',
                    'created', 'updated')
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return False
        elif obj.paid:
            return super().has_delete_permission(request, obj)
        return False

admin.site.register(Order, OrderAdmin)
# Register your models here.
