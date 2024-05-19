from .models import ShoppingCart

def cart_items_count(request):
    if request.user.is_authenticated:
        try:
            cart = ShoppingCart.objects.get(userID=request.user)
            cart_items_count = cart.cartitem_set.count()
        except ShoppingCart.DoesNotExist:
            cart_items_count = 0
    else:
        cart_items_count = 0
    return {'cart_items_count': cart_items_count}
