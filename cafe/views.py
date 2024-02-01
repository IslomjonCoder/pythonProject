from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import generics, filters
from .models import Cafe, Menu, Product, Zone, Table, Waitress, Order, OrderItem
from .serializers import (
    CafeSerializer, MenuSerializer, ProductSerializer, ZoneSerializer,
    TableSerializer, WaitressSerializer, OrderSerializer, OrderItemSerializer
)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Table


class ProductByMenuView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        menu_id = self.kwargs['menu_id']
        return Product.objects.filter(menu_id=menu_id)


class CafeListCreateView(generics.ListCreateAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer


class CafeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer


class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['cafe__id']

    def get_queryset(self):
        queryset = super().get_queryset()
        cafe_id = self.request.query_params.get('cafe_id', None)
        if cafe_id:
            queryset = queryset.filter(cafe__id=cafe_id)
        return queryset


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ZoneListCreateView(generics.ListCreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        cafe_id = self.request.query_params.get('cafe_id', None)

        # Apply filter based on cafe_id
        if cafe_id:
            queryset = queryset.filter(cafe__id=cafe_id)

        return queryset


class ZoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class TableListCreateView(generics.ListCreateAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        zone_id = self.request.query_params.get('zone_id', None)
        is_active = self.request.query_params.get('is_active', None)

        queryset = Table.objects.all()

        if zone_id:
            queryset = queryset.filter(zone_id=zone_id)

        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(active=is_active)

        return queryset


class TableDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class WaitressListCreateView(generics.ListCreateAPIView):
    serializer_class = WaitressSerializer

    def get_queryset(self):
        cafe_id = self.request.query_params.get('cafe_id', None)
        queryset = Waitress.objects.all()

        if cafe_id:
            queryset = queryset.filter(cafe_id=cafe_id)

        return queryset


class WaitressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Waitress.objects.all()
    serializer_class = WaitressSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        table_id = self.request.query_params.get('table_id', None)

        # Apply filter based on cafe_id
        if table_id:
            queryset = queryset.filter(table_id=table_id)
        return queryset


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ProductByMenuView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        menu_id = self.request.query_params.get('menu_id', None)

        # Apply filter based on cafe_id
        if menu_id:
            queryset = queryset.filter(menu_id=menu_id)
        return queryset


def update_table_and_send_message(table):
    # Update active status
    table.update_active_status()

    # Send message to WebSocket clients
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"table_{table.id}",
        {
            'type': 'table_message',
            'message': {
                'active': table.active
            }
        }
    )
from django.shortcuts import render

from  cafe.models import Room


def index_view(request):
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })


def room_view(request, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })