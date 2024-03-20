from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

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


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'


class ProfilePageView(TemplateView):
    template_name = 'user.html'

class PerfumesPageView(TemplateView):
    template_name = 'perfumes.html'

class PerfumesDetailsPageView(TemplateView):
    template_name = 'perfumesdetails.html'

class CartPageView(TemplateView):
    template_name = 'cart.html'

class OrdersPageView(TemplateView):
    template_name = 'orders.html'

class OrderDetailsPageView(TemplateView):
    template_name = 'orderdetails.html'

class PaymentPageView(TemplateView):
    template_name = 'payment.html'

class SearchResultsPageView(TemplateView):
    template_name = 'searchresults.html'

class SubscriptionPageView(TemplateView):
    template_name = 'subscription.html'

def index(request):
    return render(request, 'index.html')