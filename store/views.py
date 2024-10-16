from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def index(request):
    return render(request, 'store/index.html')

def about(request):
    return render(request, 'store/about.html')

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        )
    return render(request, 'store/product_list.html', {'products': products, 'query': query})

# CREATE: Menambahkan produk baru
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form})

# UPDATE: Mengubah produk
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diubah!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form})

# DELETE: Menghapus produk
def product_delete(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, 'Produk berhasil dihapus!')
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
