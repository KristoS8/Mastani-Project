from django.shortcuts import render, redirect, get_object_or_404
from .models import literasi
from .forms import ContactMessageForm
from seller_app.models import Product, Cart, CartItem
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render (request, "Home/index.html", {'active_page': 'home'})

def literasi_view(request):
    data_literasi = literasi.objects.all()
    context = {
        'data_literasi':data_literasi,
        'active_page':'literasi'
    }
    
    return render (request, 'Home/literasi.html', context)

def pemasaran_view(request):
    products = Product.objects.filter(seller__role='seller')

    return render (request, "Home/pemasaran.html", {'active_page':'pemasaran', 'products': products})

def about_view(request):
    return render (request, "Home/about.html", {'active_page':'about'})
from django.core.mail import send_mail

def contactus_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # Simpan form ke database
            form.save()
            # Kirim pesan sukses ke template
            return render(request, 'Home/contactus.html', {'form': form, 'success_message': 'pertanyaan atau masukan berhasil dikirim!'})
    else:
        form = ContactMessageForm()
    
    return render(request, 'Home/contactus.html', {'form': form})
def privacy_view(request):
    return render (request, "Home/privacy_policy.html", {'active_page':'privacy_policy'})

def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Periksa apakah item sudah ada di keranjang
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1  # Tambah jumlah jika sudah ada
    cart_item.save()

    return redirect("cart")

def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()  # Ambil keranjang user
    return render(request, 'Home/cart.html', {'cart': cart})

def update_cart_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
        else:
            item.delete()  # Hapus jika jumlahnya 0

    return redirect("cart")

