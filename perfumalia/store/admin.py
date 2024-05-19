from django.contrib import admin
from .models import CartItem, Perfume, ShoppingCart, User, Recommendation, Order, OrderItem, Subscription

@admin.register(Perfume, ShoppingCart, User, Recommendation, CartItem, Order, OrderItem, Subscription)
class PersonAdmin(admin.ModelAdmin):
    pass
