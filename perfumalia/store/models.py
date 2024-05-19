from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=200)
    cellphoneNumber = models.CharField(max_length=20)
    dateOfBirth = models.DateField()
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'address', 'cellphoneNumber', 'dateOfBirth']

    def __str__(self):
        return self.email
class Perfume(models.Model):
    productID = models.CharField(primary_key = True, max_length=100)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventoryQuantity = models.IntegerField()
    details = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def update_inventory(self, new_quantity):
        """Actualiza la cantidad de inventario de un perfume."""
        self.inventoryQuantity = new_quantity
        self.save()

    def view_details(self):
        """Muestra los detalles de un perfume."""
        return f"{self.name} by {self.author} is a {self.category} perfume by {self.brand}. {self.details}"
    
    
    def calculate_price(self, quantity):
        """Calcula el precio total de una cantidad de perfumes."""
        return self.price * quantity
    

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    orderItems = models.ManyToManyField(Perfume, through='OrderItem')
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orderStatus = models.CharField(max_length=50)
    orderDate = models.DateField(auto_now_add=True)

class OrderItem(models.Model):
    perfumeID = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    totalPrice = models.IntegerField(null = True)

class ShoppingCart(models.Model):
    userID = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    savedForLater = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)
    
    def update_subtotal(self):
        """Actualiza el subtotal del carrito basado en los ítems actuales."""
        self.subtotal = sum(item.calcular_total() for item in self.cartitem_set.all())
        self.save()

    def save_for_later(self, item_id):
        """Guarda un artículo para después."""
        # Mueve un artículo de 'items' a 'savedForLater'
        for item in self.items:
            if item['id'] == item_id:  
                self.items.remove(item)
                self.savedForLater.append(item)
                self.save()
                return item  # Retorna el ítem movido
        return None  # Retorna None si el ítem no se encontró
    
    def clear_cart(self):
        """Vacía el carrito."""
        self.items = []
        self.subtotal = 0
        self.save()

 
    def checkout(self):
        with transaction.atomic():
            # Crear un nuevo pedido
            new_order = Order.objects.create(
                userID=self.userID,
                orderStatus='Pending',  # O cualquier estado inicial que prefieras
                shippingDetails={},  # Asume valores predeterminados o ajusta según sea necesario
                orderHistory={}  # Asume valores predeterminados o ajusta según sea necesario
            )

            # Transferir ítems de ShoppingCart a Order
            for item in self.cartitem_set.all():
                OrderItem.objects.create(
                    perfume=item.product,  # Asume que 'product' ahora es un objeto Perfume en CartItem
                    cantidad=item.quantity,
                    orderID=new_order
                )

                # Actualizar inventario del perfume asociado
                item.product.update_inventory(item.product.inventoryQuantity - item.quantity)

                # Eliminar el CartItem ya que ha sido transferido a OrderItem
                item.delete()

            # Vaciar atributos del carrito de compras
            self.subtotal = 0
            self.savedForLater.clear()  # Asume que quieres limpiar la lista de 'guardar para más tarde'
            self.save()  # No olvides guardar cualquier cambio en el carrito

            # Devuelve el pedido para su posterior procesamiento
            return new_order
    
class Recommendation(models.Model):
    userID = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key = True)
    purchaseHistory = models.JSONField(blank=True, default=list)
    browsingHistory = models.JSONField(blank=True, default=list)
    recommendationList = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)
    
    def add_to_purchase_history(self, perfume):
        """Agrega detalles de un perfume al historial de compras."""
        history = self.purchaseHistory or []
        perfume_details = {
            'name': perfume.name,
            'details': perfume.details,
            'category': perfume.category,
            'brand': perfume.brand,
            'author': perfume.author
        }
        history.insert(0, perfume_details)
        self.purchaseHistory = history
        self.save()

    def add_to_browsing_history(self, perfume):
        """Agrega detalles de un perfume al historial de navegación."""
        history = self.browsingHistory or []
        perfume_details = {
            'name': perfume.name,
            'details': perfume.details,
            'category': perfume.category,
            'brand': perfume.brand,
            'author': perfume.author
        }
        history.insert(0, perfume_details)
        self.browsingHistory = history
        self.save()
    
    def update_recommendation_list(self, new_recommendations):
        """Fusiona una nueva lista de recomendaciones con la antigua."""
        existing_recommendations = self.recommendationList or []
        existing_dict = {rec['name']: rec for rec in existing_recommendations} # Crea un diccionario para verificación rápida

        for new_rec in new_recommendations: # Agrega solo las recomendaciones que no estén ya en la lista
            if new_rec['name'] not in existing_dict:
                existing_recommendations.append(new_rec)
                existing_dict[new_rec['name']] = new_rec  # Actualiza el diccionario para futuras verificaciones

        self.recommendationList = existing_recommendations
        self.save()

class CartItem(models.Model):
    product = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.product)
    
    def actualizar_cantidad(self, nueva_cantidad):
        """Actualiza la cantidad de un artículo en el carrito."""
        if nueva_cantidad >= 0:
            self.quantity = nueva_cantidad
            self.save()
            self.shoppingCart.update_subtotal()

    def calcular_total(self):
        """Calcula el precio total de un artículo."""
        return self.product.price * self.quantity
    
    def obtener_precio_unitario(self):
        """Obtiene el precio unitario de un artículo."""
        return self.product.price # Precio unitario
    
    def obtener_precio_total(self):
        """Obtiene el precio total de un artículo."""
        return self.calcular_total()
    
class Subscription(models.Model):
    subscriptionID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscriptionStatus = models.CharField(max_length=50)
    subscriptionType = models.CharField(max_length=100)
    billingDate = models.DateField()