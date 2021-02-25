from django.db import models
from django.contrib.auth.models import User

from location_field.models.plain import PlainLocationField


class Client(models.Model):
    b_user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    balance = models.IntegerField(default=0)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    location = PlainLocationField(based_fields=['Uzbekistan'], zoom=7)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.b_user.username


class Merchant(models.Model):
    b_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant')
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    location = PlainLocationField(based_fields=['Uzbekistan'], zoom=7)
    role = models.CharField(max_length=15)

    def __str__(self):
        return self.b_user.username


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def get_total(self):
        products = self.product_set.all()
        total = sum(products)
        return total

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='image', null=True)
    slug = models.SlugField(max_length=50)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    quantity = models.IntegerField()
    old_price = models.DecimalField(max_digits=16, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    bank = models.CharField(max_length=25)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_cart_total(self):
        cart_item = self.cartitem_set.all()
        total = sum([item.get_total for item in cart_item])
        return total

    @property
    def get_total(self):
        cart_item = self.cartitem_set.all()
        total = sum(item.quantity for item in cart_item)
        return total

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
        
    @property
    def get_total(self):
        return self.product.price * self.quantity