from django import forms
from .models import Perfume, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'address', 'cellphoneNumber', 'dateOfBirth']

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