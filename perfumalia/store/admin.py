from django.contrib import admin
from .models import CartItem, Perfume, ShoppingCart, User, Recommendations

@admin.register(Perfume, ShoppingCart, User, Recommendations, CartItem)
class PersonAdmin(admin.ModelAdmin):
    pass
