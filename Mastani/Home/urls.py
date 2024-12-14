from django.urls import path, include # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('literasi/', views.literasi_view, name='literasi'),
    path('pembeli/pemasaran/', views.pemasaran_view, name="pemasaran"),
    path('about/', views.about_view, name='about'),
    path('contactus/', views.contactus_view, name='contactus'),
    path('privacy_policy/', views.privacy_view, name='privacy_policy'),
    path('cart/', views.cart_detail, name='cart'),  
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
]