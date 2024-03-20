from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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

def index(request):
    return render(request, 'index.html')