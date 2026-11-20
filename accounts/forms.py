from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import FridgeItem, User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'profile_photo',
        ]

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if email and User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                'This email is already in use by another account.'
            )
        return email


class FridgeItemForm(forms.ModelForm):

    class Meta:
        model = FridgeItem
        fields = [
            'name',
            'category',
            'zone',
            'quantity',
            'unit',
            'expiry_date',
        ]
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError('Item name is required.')
        return name

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return quantity

    def clean_expiry_date(self):
        expiry = self.cleaned_data.get('expiry_date')
        if expiry and expiry < date(2000, 1, 1):
            raise forms.ValidationError('Please enter a valid expiry date.')
        return expiry