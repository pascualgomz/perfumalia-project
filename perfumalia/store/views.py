from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from store.models import Perfume, User
from store.forms import UserForm, LoginForm

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'

class LoginPageView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

class SingUpPageView(TemplateView):
    template_name = 'singup.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

class ProfilePageView(TemplateView):
    template_name = 'user.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {'user': user})

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

def admin_login(request):
    return render(request, 'admin/login.html')
