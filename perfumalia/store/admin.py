from django.contrib import admin
from .models import CartItem, Perfume, ShoppingCart, User, Recommendations, Order, OrderItem, Subscription

@admin.register(Perfume, ShoppingCart, User, Recommendations, CartItem, Order, OrderItem, Subscription)
class PersonAdmin(admin.ModelAdmin):
    pass
