from django import forms
from .models import User, Perfume
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    dateOfBirth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2021)))

    class Meta:
        model = User
        fields = ['name', 'email', 'address', 'cellphoneNumber', 'dateOfBirth', 'password']

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("The password confirmation does not match")

        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PerfumeForm(forms.ModelForm):
    class Meta:
        model = Perfume
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return price

    def clean_inventory_quantity(self):
        inventory_quantity = self.cleaned_data['inventory_quantity']
        if inventory_quantity < 0:
            raise forms.ValidationError("La cantidad en inventario no puede ser negativa.")
        return inventory_quantity
