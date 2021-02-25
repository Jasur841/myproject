from django.conf.urls import url
from django.urls import path

# from myproject.marketapp.views import index, sign_up
from .views import index, login_view, sign_up, logout_view, base, profile, advertisement, balance,\
    add_balance,product_detail, cart,ordered_cart,category_by_name

urlpatterns = [
    path('', index, name='index'),
    path('signup/', sign_up, name='signup'),
    path('login_view/', login_view, name='login_view'),
    url(r'logout/$', logout_view, name='logout_view'),
    path('base/', base, name='base'),
    path('profile/', profile, name='profile'),
    path('advertisement/', advertisement, name='advertisement'),
    path('balance/', balance, name='balance'),
    path('add-balance/', add_balance, name='add_balance'),
    path('product/<str:slug>', product_detail, name='product-view'),
    path('cart/', cart, name='cart'),
    path('ordered_carts/', ordered_cart, name='ordered_carts'),
    path('category/<str:slug>', category_by_name, name='category-by-name'),
]
