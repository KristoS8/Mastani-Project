from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('keuangan/', views.keuangan_view, name='keuangan_view'),
    path('riwayatPdf/', views.generate_riwayat_pdf, name='generate_riwayat_pdf'),
    path('transferSaldo/', views.transfer_saldo, name='transfer_saldo'),
    path('isipulsa/', views.isi_pulsa, name='isi_pulsa'),
]