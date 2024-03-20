from django.core.management.base import BaseCommand 
from store.factories import UserFactory, PerfumeFactory, OrderFactory, OrderItemFactory, ShoppingCartFactory, RecommendationsFactory, CartItemFactory, SubscriptionFactory 

class Command(BaseCommand): 
    help = 'Seed the database with products' 
    def handle(self, *args, **kwargs): 
        # Crea 8 instancias de cada modelo
        users = UserFactory.create_batch(8)
        perfumes = PerfumeFactory.create_batch(8)
        orders = OrderFactory.create_batch(8)
        order_items = OrderItemFactory.create_batch(8)
        shopping_carts = ShoppingCartFactory.create_batch(8)
        recommendations = RecommendationsFactory.create_batch(8)
        cart_items = CartItemFactory.create_batch(8)
        subscriptions = SubscriptionFactory.create_batch(8)

    # Puedes hacer más manipulaciones de los datos aquí si es necesario
        self.stdout.write(self.style.SUCCESS('Successfully seeded products')) 