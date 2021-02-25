from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.exceptions import ValidationError
from marketapp.forms import SignUpForm, LoginForm, AddProductForm, AddBalanceForm, EditCartItem
from marketapp.models import Product, Category, Client, Merchant, User, Transaction, CartItem, Cart
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib import messages


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'main.html', {
        'products': products,
        "categories": categories
    })


@login_required(login_url='signup')
def base(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'index.html', {
        'products': products,
        "categories": categories
    })


def sign_up(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(data=request.POST, files=request.FILES)
        if sign_up_form.is_valid():
            sign_up_form.save()
            username = sign_up_form.data['username']
            password = sign_up_form.data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                # raise ValidationError("Error")
                return redirect('signup')
        else:
            return HttpResponse('<h1>This user authenticated ago please create new user')
    else:
        sign_up_form = SignUpForm()
    return render(request, 'signup.html', {
        'sign_up_form': sign_up_form
    })


def login_view(request):
    login_form = LoginForm()
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('base')
        return render(request, 'login.html', {'login_form': login_form})
    else:
        return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect(index)


@login_required(login_url='login_view')
def profile(request):
    return render(request, 'profile.html')


def advertisement(request, add_product_form=None):
    add_product_form = AddProductForm()
    if request.method == 'POST':
        if request.user.merchant.role == 'merchant':
            add_product_form = AddProductForm(initial={'merchant': request.user.merchant.pk}, data=request.POST,
                                              files=request.FILES)
            if add_product_form.is_valid():
                add_product_form.save()
        return render(request, 'main.html')
    return render(request, 'add_product.html', {'add_product_form': add_product_form})


def balance(request):
    balance = User.objects.all()
    return render(request, 'balance.html', {
        'balance': balance
    })


def add_balance(request):
    if request.method == 'POST':
        add_balance = AddBalanceForm(data=request.POST)
        if add_balance.is_valid():
            user = Client.objects.filter(pk=request.user.client.pk).first()
            permission = True
            if permission is True:
                user.balance = request.user.client.balance + int(add_balance.data['value'])
                user.save()
                Transaction.objects.create(user=request.user.client, value=int(add_balance.data['value']),
                                           bank=add_balance.data['type'])
            else:
                return render(request, 'permission_error.html')
        return redirect(base)
    else:
        add_balance = AddBalanceForm()
        return render(request, 'addbalance.html', {'add_balance': add_balance})


@login_required(login_url=sign_up)
def cart(request):
    user_cart = Cart.objects.filter(user=request.user.client, is_ordered=False, is_success=False).first()
    cart_items = CartItem.objects.filter(cart=user_cart)
    if request.method == 'POST':

        if request.POST['action'] == 'delete':
            product = get_object_or_404(CartItem, id=int(request.POST['product_id']))
            product.delete()

            return redirect('cart')
        
        elif request.POST['action'] == 'order':
            if request.user.client.balance >= user_cart.get_cart_total:
                user = get_object_or_404(Client, id=request.user.client.id)
                user_cart.is_ordered = True
                user_cart.ordered_date = datetime.now()
                user_cart.save()
                user.balance -= user_cart.get_cart_total
                user.save()

                Transaction.objects.create(user=request.user.client, bank='MarketPlace', value=user_cart.get_cart_total)
                messages.success(request, 'Your ordered updated successfully!')

                return redirect(base)

            else:
                return redirect('balance_error')

    else:
        return render(request, 'cart.html', {'user_cart': user_cart, 'cart_items': cart_items})


def product_detail(request, slug):
    product = Product.objects.filter(slug=slug).first()
    if not request.user.is_authenticated:
        if request.method == 'POST':
            return redirect(sign_up)
        return render(request, 'product_detail_page.html', {'product': product})
    else:
        user_cart = Cart.objects.filter(user=request.user.client, is_success=False, is_ordered=False).first()
        cart_item = CartItem.objects.filter(cart=user_cart, product=product).first()

        if request.method == 'POST':
            edit_cart_form = EditCartItem(request.POST)
            if cart_item is None:
                if user_cart is None:
                    user_cart = Cart.objects.create(user=request.user.client)
                cart_item = CartItem.objects.create(product=product, cart=user_cart, quantity=1)
            else:
                if edit_cart_form.is_valid():
                    cart_item.quantity = edit_cart_form.data['quantity']
                    cart_item.save()
                    if edit_cart_form.data['quantity'] == '0':
                        cart_item.delete()
                        return redirect(cart)
                    return redirect(base)
        if cart_item is not None:
            edit_cart_form = EditCartItem(initial={'quantity': cart_item.quantity})
        else:
            edit_cart_form = EditCartItem()
        return render(request, 'product_detail_page.html',
                      {'product': product, 'cart_item': cart_item, 'edit_cart_form': edit_cart_form})


def ordered_cart(request):
    ordered_carts = Cart.objects.filter(user=request.user.client)
    return render(request, 'ordered_carts.html', {'ordered_carts': ordered_carts})


def balance_error(request):
    return render(request, 'balance_error.html')


@login_required(login_url=index)
def category_by_name(request, slug):
    category = Category.objects.filter(slug=slug).first()
    products = Product.objects.filter(category=category)
    return render(request, 'product_by_category.html', {'products': products, 'category': category})
