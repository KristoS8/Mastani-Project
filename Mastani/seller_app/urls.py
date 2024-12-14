from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='seller_dashboard'),
    path('profile/', views.profile_view, name='profile_seller'),
    path('produk/', views.product_list, name='product_list'),
    path('produk/tambah/', views.add_product, name='add_product'),
    path('produk/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('produk/hapus/<int:product_id>/', views.delete_product, name='delete_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
