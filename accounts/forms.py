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

    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner

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
        if len(name) < 2:
            raise forms.ValidationError('Item name must contain at least 2 characters.')
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

    def clean(self):
        cleaned_data = super().clean()
        owner = self.owner or getattr(self.instance, 'owner', None)
        if owner is None:
            return cleaned_data

        name = cleaned_data.get('name')
        zone = cleaned_data.get('zone')
        unit = cleaned_data.get('unit')
        expiry_date = cleaned_data.get('expiry_date')

        if name and zone and unit:
            duplicates = FridgeItem.objects.filter(
                owner=owner,
                name__iexact=name,
                zone=zone,
                unit__iexact=unit,
                expiry_date=expiry_date,
            )
            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)
            if duplicates.exists():
                raise forms.ValidationError(
                    'An identical fridge item already exists.'
                )

        return cleaned_data