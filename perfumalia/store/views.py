from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from store.models import Order, Perfume, ShoppingCart, Subscription, User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

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
        carts = ShoppingCart.objects.all()
        return render(request, self.template_name, {'carts': carts})

class OrdersPageView(TemplateView):
    template_name = 'orders.html'

    def get(self, request):
        orders = Order.objects.all()
        return render(request, self.template_name, {'orders': orders})

class OrderDetailsPageView(TemplateView):
    template_name = 'orderdetails.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, self.template_name, {'order': order})

class SearchResultsPageView(TemplateView):
    template_name = 'searchresults.html'

    def get(self, request, query):
        resultados = Perfume.objects.filter(name__icontains=query)
        return render(request, self.template_name, {'perfumes': resultados})

class SubscriptionPageView(TemplateView):
    template_name = 'subscription.html'

    def get(self, request):
        subscriptions = Subscription.objects.all()
        return render(request, self.template_name, {'subscriptions': subscriptions})

def index(request):
    return render(request, 'index.html')