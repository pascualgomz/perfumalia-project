from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from store.models import Order, Perfume, ShoppingCart, Subscription, User
from django.contrib.auth import logout
from django.views import View
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from newsapi import NewsApiClient

##################################################### Dependency Inversion
# For PDF
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.timezone import now
# For Inversion
from .services import *
from .interfaces import *

def generar_cheque(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Usar el servicio por medio de la interfaz
    pdf_manager = PDFManager()
    pdf_service = PDF_Service(pdf_manager)

    # Datos
    # Obtener el usuario actual
    user = request.user
    # Obtener el carrito de compras asociado al usuario actual
    try:
        cart = ShoppingCart.objects.get(userID=user)
    except ShoppingCart.DoesNotExist:
        return HttpResponse("No se encontró un carrito de compras para el usuario actual.", status=404)
    
    # Datos
    datos = {
        'nombre': user.name,
        'direccion': user.address,
        'cel': user.cellphoneNumber,
        'total': cart.subtotal,
        'fecha': now().strftime('%d/%m/%y')
    }
    
    response = pdf_service.create_Check(datos)
    return response

class AddToCartView(View):
    def post(self, request, productID):
        perfume = get_object_or_404(Perfume, productID=productID)
        user = request.user
        cart, created = ShoppingCart.objects.get_or_create(userID=user)
        cart_item, created = CartItem.objects.get_or_create(product=perfume, shoppingCart=cart)
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1  # Añadir esto para asegurar que quantity tenga un valor
        cart_item.save()
        cart.update_subtotal()
        return redirect('perfumes')
    
    
class RemoveFromCartView(View):
    def post(self, request, productID):
        perfume = get_object_or_404(Perfume, productID=productID)
        user = request.user
        cart = get_object_or_404(ShoppingCart, userID=user)
        cart_item = get_object_or_404(CartItem, product=perfume, shoppingCart=cart)
        cart_item.delete()
        cart.update_subtotal()
        return redirect('cart')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def LogoutView(request):
    logout(request)
    return redirect('logout_success')


def LogoutSuccessView(request):
    return render(request, 'logout.html')

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'user/login.html'  
    next_page = reverse_lazy('/')
    redirect_authenticated_user = True 

class HomePageView(TemplateView):
    template_name = 'home.html'


class ProfilePageView(TemplateView):
    template_name = 'user.html'

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {'users': users})

class PerfumesPageView(TemplateView):
    template_name = 'perfumes.html'

    def get(self, request):
        perfumes = Perfume.objects.all()
        return render(request, self.template_name, {'perfumes': perfumes})

class PerfumesDetailsPageView(TemplateView):
    template_name = 'perfumesdetails.html'

    def get(self, request, pk):
        perfume = get_object_or_404(Perfume, pk=pk)
        return render(request, self.template_name, {'perfume': perfume})

class CartPageView(TemplateView):
    template_name = 'cart.html'

    def get(self, request):
        try:
            cart = ShoppingCart.objects.get(userID=request.user)
        except ShoppingCart.DoesNotExist:
            cart = None
        return render(request, self.template_name, {'carts': cart})

@method_decorator(login_required, name='dispatch')
class OrdersPageView(TemplateView):
    template_name = 'orders.html'

    def get(self, request):
        orders = Order.objects.filter(userID=request.user)
        return render(request, self.template_name, {'orders': orders})


@method_decorator(login_required, name='dispatch')
class CompleteOrderView(View):
    def post(self, request):
        user = request.user
        cart = get_object_or_404(ShoppingCart, userID=user)
        order = Order.objects.create(
            userID=user,
            orderStatus='Completed'  # O el estado inicial que prefieras
        )

        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                perfumeID=cart_item.product,
                quantity=cart_item.quantity,
                orderID=order,
                totalPrice=cart_item.calcular_total()
            )
            cart_item.delete()

        cart.update_subtotal()  # Actualiza el subtotal del carrito después de eliminar los artículos
        return redirect('payment')



@method_decorator(login_required, name='dispatch')
class OrderDetailsPageView(TemplateView):
    template_name = 'orderdetails.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, userID=request.user)
        return render(request, self.template_name, {'order': order})

class SearchResultsPageView(TemplateView):
    template_name = 'searchresults.html'

    def get(self, request, query):
        resultados = Perfume.objects.filter(name__icontains=query)
        return render(request, self.template_name, {'perfumes': resultados})

@method_decorator(login_required, name='dispatch')
class SubscriptionsPageView(TemplateView):
    template_name = 'subscriptions.html'

    def get(self, request):
        subscriptions = Subscription.objects.filter(userID=request.user)
        return render(request, self.template_name, {'subscriptions': subscriptions})

class SubscriptionDetailsPageView(TemplateView):
    template_name = 'subscriptiondetails.html'

    def get(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk, userID=request.user)
        return render(request, self.template_name, {'subscription': subscription})

@method_decorator(login_required, name='dispatch')
class SubscriptionPlansPageView(TemplateView):
    template_name = 'subscriptionplans.html'

    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        return render(request, self.template_name, {'plans': plans})

@method_decorator(login_required, name='dispatch')
class SubscribeView(View):
    def post(self, request, planID):
        user = request.user
        existing_subscription = Subscription.objects.filter(userID=user, subscriptionStatus='Active').first()
        if existing_subscription:
            # El usuario ya tiene una suscripción activa, no puede suscribirse a otra
            return redirect('subscriptions')

        plan = get_object_or_404(SubscriptionPlan, pk=planID)
        billing_date = timezone.now().date()
        expiration_date = billing_date + relativedelta(months=1)

        subscription = Subscription.objects.create(
            userID=user,
            plan=plan,
            subscriptionType=plan.name,
            subscriptionStatus='Active',
            billingDate=billing_date,
            expirationDate=expiration_date
        )
        return redirect('subscriptiondetails', pk=subscription.subscriptionID)

@method_decorator(login_required, name='dispatch')
class CancelSubscriptionView(View):
    def post(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk, userID=request.user)
        subscription.subscriptionStatus = 'Cancelled'
        subscription.save()
        return redirect('subscriptions')

@method_decorator(login_required, name='dispatch')
class PaymentPageView(View):
    def get(self, request):
        return render(request, 'payment.html')
    
class NewsPageView(View):
    template_name = 'news.html'

    def get(self, request):
        newsapi = NewsApiClient(api_key='74f6025f04a84240829c4f89dfbd990a')
        articles = newsapi.get_everything(q='beauty',
                                      sort_by='relevancy',
                                      page=2)
        return render(request, self.template_name, {'articles': articles.get('articles', [])})