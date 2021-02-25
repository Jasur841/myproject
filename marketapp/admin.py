from django.contrib import admin
from .models import Category, Product, Client, Transaction, Cart, CartItem, Merchant

# Register your models here.

admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(CartItem)



admin.site.register(Client)
admin.site.register(Merchant)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    prepopulated_fields = {"slug": ('name',)}
