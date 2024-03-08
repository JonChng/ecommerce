from django.contrib import admin
from .models import Item, Cart, Order, OrderItem

# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
