from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from rest_framework.authtoken.models import Token


class Cafe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='cafe_logos/', null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^\+?998\d{9,15}$',
                message="Phone number must be entered in the format: '+998XXXXXXXXX'. Up to 15 digits allowed.",
            )
        ],
    )
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    director_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=255)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.cafe}"


class Table(models.Model):
    number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)  # Added "active" field

    def __str__(self):
        return f"{self.zone} - {self.number}{' (Active)' if self.active else ''}"

    def update_active_status(self):
        # Check if there are any active orders for this table
        active_orders = self.order_set.filter(is_active=True).exists()

        # Update the active status based on the presence of active orders
        self.active = active_orders
        self.save()


class Waitress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='waitress', help_text="Enter the user.")
    contact_number = models.CharField(max_length=15)
    employee_id = models.CharField(max_length=20, unique=True, blank=False, null=False,
                                   validators=[RegexValidator(r'^[a-zA-Z0-9]*$',
                                                              'Employee ID must contain only alphanumeric characters.')])
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    notes = models.TextField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} items"


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    waitress = models.ForeignKey(Waitress, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cafe = models.ForeignKey("Cafe", on_delete=models.CASCADE)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Set the cafe field to the menu's cafe
        if self.waitress and self.waitress.cafe:
            self.cafe = self.waitress.cafe

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.waitress.user.username}"


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total_price(sender, instance, **kwargs):
    order = instance.order
    order_items = order.orderitem_set.all()
    total_price = order_items.aggregate(total_price=Coalesce(Sum(F('quantity') * F('product__price')), 0))[
        'total_price']
    order.total_price = total_price
    order.save()


@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
def update_table_active_status(sender, instance, **kwargs):
    table = instance.table
    orders_count = Order.objects.filter(table=table).count()

    # Update the active status based on the presence of active orders
    table.active = orders_count > 0
    table.save()

from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'