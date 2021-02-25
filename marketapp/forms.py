from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Product, User, Category, CartItem, Merchant, Client


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, help_text='*Not Required*',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=[('merchant', 'Merchant'), ('client', 'Client')])
    phone_number = forms.CharField(max_length=20)
    location = forms.CharField(max_length=110)
    image = forms.ImageField(required=False)

    def clean_password1(self):
        password1 = self.data['password']
        password2 = self.data['password2']

        if password1 != password2:
            raise ValidationError('Password doesn\'t match!')
        return password1

    def save(self):
        base_user = User.objects.create_user(username=self.data['username'], password=self.data['password'],
                                             email=self.data['email'])
        if self.data['role'] == 'merchant':
            Merchant.objects.create(b_user=base_user, phone_number=self.data['phone_number'],
                                    location=self.data['location'], image=self.files['image'], role=self.data['role'])
        else:
            Client.objects.create(b_user=base_user, phone_number=self.data['phone_number'],
                                  location=self.data['location'], image=self.files['image'], role=self.data['role'])


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddProductForm(forms.ModelForm):
    name = forms.CharField(max_length=40)
    description = forms.CharField(max_length=155)
    image = forms.ImageField()
    slug = forms.SlugField()
    price = forms.DecimalField(max_digits=16, decimal_places=2)
    quantity = forms.IntegerField()
    old_price = forms.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        model = Product
        fields = '__all__'

    def save(self, commit=True):
        category = Category.objects.filter(pk=self.data['category']).first()
        merchant = Merchant.objects.filter(id=self.initial['merchant']).first()
        product = Product.objects.create(category=category, name=self.data['name'],
                                         description=self.data['description'], image=self.files['image'],
                                         slug=self.data['name'],
                                         price=self.data['price'], quantity=self.data['quantity'],
                                         old_price=self.data['old_price'], merchant=merchant)
        return product


class AddBalanceForm(forms.Form):
    type = forms.ChoiceField(choices=[('humo', 'Humo'), ('uzcard', 'Uzcard')])
    cart_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                     label='Karta raqamini kiriting:')
    value = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Value')


class EditCartItem(forms.Form):
    quantity = forms.IntegerField(min_value=0,
                                  widget=forms.TextInput(attrs={'id': 'quantity', 'style': 'width: 50px'}))

    class Meta:
        model = CartItem

class CartForm(forms.Form):
    product = forms.CharField(max_length=200, disabled=True)