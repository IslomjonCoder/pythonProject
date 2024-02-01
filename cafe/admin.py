from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cafe, Menu, Product, Zone, Table, Waitress, Order, OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__table__zone']
    search_fields = ['order__waitress__user__username', 'order__table__number']
    exclude = ['price']


class OrderAdmin(admin.ModelAdmin):
    # inlines = [OrderItemInline]
    list_display = ['table', 'waitress', 'created_at', 'total_price']
    list_filter = ['table__zone', 'created_at']
    search_fields = ['waitress__user__username', 'table__number']
    exclude = ['total_price','cafe']



class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'zone', 'active']
    list_filter = ['zone', 'active']
    search_fields = ['number']


class WaitressAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_number', 'employee_id', 'cafe']
    search_fields = ['user__username', 'employee_id']


class CafeAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'location', 'created_at', 'director_name']
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu', 'price']
    search_fields = ['name']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'cafe']
    search_fields = ['name']
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'cafe']

# Register your models with the custom admin classes
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Waitress, WaitressAdmin)
admin.site.register(Cafe, CafeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Zone,ZoneAdmin)
from cafe.models import Room, Message

admin.site.register(Room)
admin.site.register(Message)