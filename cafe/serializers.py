from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cafe, Menu, Product, Zone, Table, Waitress, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ['id', 'name', 'logo', 'phone_number', 'location', 'created_at', 'director_name']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'image', 'cafe']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'menu', 'image']


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name', 'cafe']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'capacity', 'zone', 'active']


class WaitressSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Waitress
        fields = ['id', 'user', 'contact_number', 'employee_id', 'cafe']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'notes', 'price']


class OrderSerializer(serializers.ModelSerializer):
    waitress = WaitressSerializer()
    table = TableSerializer()
    orderitem_set = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'waitress', 'created_at', 'cafe', 'total_price', 'orderitem_set']
