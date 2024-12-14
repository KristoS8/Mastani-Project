from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserRegistForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','no_telp', 'email','password1','password2','role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(attrs={'class':'form-select','id':'role'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['no_telp', 'role']