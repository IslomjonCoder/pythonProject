# urls.py

from django.urls import path

from . import consumers, views
from .views import (
    CafeListCreateView, CafeDetailView,
    MenuListCreateView, MenuDetailView,
    ProductListCreateView, ProductDetailView,
    ZoneListCreateView, ZoneDetailView,
    TableListCreateView, TableDetailView,
    WaitressListCreateView, WaitressDetailView,
    OrderListCreateView, OrderDetailView,
    OrderItemListCreateView, OrderItemDetailView, ProductByMenuView
)

urlpatterns = [

    # path('cafes/', CafeListCreateView.as_view(), name='cafe-list-create'),
    # path('cafes/<int:pk>/', CafeDetailView.as_view(), name='cafe-detail'),
    #
    # path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    # path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
    #
    # path('products/', ProductByMenuView.as_view(), name='product-list-create'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    #
    # path('zones/', ZoneListCreateView.as_view(), name='zone-list-create'),
    # path('zones/<int:pk>/', ZoneDetailView.as_view(), name='zone-detail'),
    #
    # path('tables/', TableListCreateView.as_view(), name='table-list-create'),
    # path('tables/<int:pk>/', TableDetailView.as_view(), name='table-detail'),
    #
    # path('waitresses/', WaitressListCreateView.as_view(), name='waitress-list-create'),
    # path('waitresses/<int:pk>/', WaitressDetailView.as_view(), name='waitress-detail'),
    #
    # path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    # path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    #
    # path('order-items/', OrderItemListCreateView.as_view(), name='order-item-list-create'),
    # path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='order-item-detail'),
    #
    # path('menu/<int:menu_id>/products/', ProductByMenuView.as_view(), name='products-by-menu'),
    path('', views.lobby, name='chat-index'),
    path('<str:room_name>/', views.room_view, name='chat-room'),

]