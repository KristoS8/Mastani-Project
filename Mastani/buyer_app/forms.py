from django import forms
from auth_user.models import CustomUser

class UpdateUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','no_telp','email']


class TopUpForm(forms.Form):
    nominal = forms.ChoiceField(
        choices=[
            (10000, 'Rp. 10.000'),
            (15000, 'Rp. 15.000'),
            (20000, 'Rp. 20.000'),
            (30000, 'Rp. 30.000'),
            (50000, 'Rp. 50.000'),
        ],
        widget=forms.RadioSelect
    )

    payment_method = forms.ChoiceField(
        choices=[
            ('Telkomsel','Telkomsel'),
            ('Bank_BRI','BANK_BRI'),
        ],
        widget=forms.RadioSelect
    )
