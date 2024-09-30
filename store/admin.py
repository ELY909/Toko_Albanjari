from django.contrib import admin
from .models import Category, Product, Customer, Order

# Menambahkan semua model ke admin site
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('categories',)
    filter_horizontal = ('categories',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email')

    # Aksi custom: Otomatis buat Order ketika Customer baru dibuat
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Jika belum ada order untuk customer, otomatis buat
        if not Order.objects.filter(customer=obj).exists():
            order = Order(customer=obj)
            order.save()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date')
    search_fields = ('customer__name',)
    filter_horizontal = ('product',)
