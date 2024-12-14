from django import forms
from .models import Product  # Pastikan Product diimpor dari models

from auth_user.models import CustomUser

class UpdateSeller(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','no_telp','email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'quantity', 'price']