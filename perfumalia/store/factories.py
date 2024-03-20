import factory
from .models import User, Perfume, Order, OrderItem, ShoppingCart, Recommendations, CartItem, Subscription
from django.contrib.auth.hashers import make_password
from datetime import datetime

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    address = factory.Faker('address')
    cellphoneNumber = factory.Faker('phone_number')
    dateOfBirth = factory.Faker('date_of_birth')
    password = make_password('password123')  # Puedes establecer una contraseña predefinida

class PerfumeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Perfume

    productID = factory.Sequence(lambda n: f'perfume-{n}')
    name = factory.Faker('word')
    author = factory.Faker('name')
    brand = factory.Faker('company')
    category = factory.Faker('word')
    price = factory.Faker('random_number', digits=2)
    inventoryQuantity = factory.Faker('random_number', digits=2)
    details = factory.Faker('text')

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    userID = factory.SubFactory(UserFactory)
    orderStatus = factory.Faker('word')
    orderDate = datetime.now()

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    perfumeID = factory.SubFactory(PerfumeFactory)
    quantity = factory.Faker('random_number', digits=1)
    orderID = factory.SubFactory(OrderFactory)
    totalPrice = factory.Faker('random_number', digits=2)

class ShoppingCartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingCart

    userID = factory.SubFactory(UserFactory)
    subtotal = factory.Faker('random_number', digits=2)

class RecommendationsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recommendations

    userID = factory.SubFactory(UserFactory)
    purchaseHistory = {}
    browsingHistory = {}
    recommendationList = {}

class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    product = factory.SubFactory(PerfumeFactory)
    shoppingCart = factory.SubFactory(ShoppingCartFactory)
    quantity = factory.Faker('random_number', digits=1)

class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    userID = factory.SubFactory(UserFactory)
    subscriptionStatus = factory.Faker('word')
    subscriptionType = factory.Faker('word')
    billingDate = factory.Faker('date_this_year')