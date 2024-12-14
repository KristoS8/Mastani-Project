from django.shortcuts import render, redirect
from .forms import UpdateSeller
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.shortcuts import get_object_or_404


# Create your views here.

def dashboard (request):
    if request.user.is_authenticated:
        user = request.user

    else:
        user = None

    total_products = Product.objects.filter(seller=request.user).count()

    return render(request, 'seller_app/dashboard.html', {'user':user, 'total_products':total_products, 'active_page':'dashboard'})

def profile_view(request):
   # update user data

    user_auth = request.user

    if request.method == 'POST':
        form = UpdateSeller(request.POST, instance=user_auth)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Anda Telah Di Perbaharui!')
            return redirect('profile_view')
    else:
        form = UpdateSeller(instance=user_auth)


    return render(request, 'seller_app/profile.html', {'form':form, 'active_page':'profile'} )


def product_list(request):
    products = Product.objects.all()
    return render(request, 'seller_app/product_list.html', {'products': products, 'active_page':'product'})

# Menambahkan produk baru
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Use request.FILES if you are uploading files (images)
        if form.is_valid():
            products = form.save(commit=False)
            products.seller = request.user
            products.save()
            return redirect('product_list')  # Or any other view you'd like to redirect after saving
    else:
        form = ProductForm()

    return render(request, 'seller_app/add_product.html', {'form': form})

# Mengedit produk
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diperbarui!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'seller_app/edit_product.html', {'form': form, 'product': product})

# Menghapus produk
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('product_list')