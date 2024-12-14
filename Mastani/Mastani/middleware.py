from django.shortcuts import render,redirect
from django.http import HttpResponseForbidden

class RoleBaseAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/auth/complete_profile/'):
            return self.get_response(request)
        
        if not request.user.is_authenticated:
            if request.path.startswith('/pembeli/') or request.path.startswith('/penjual/'):
                return redirect('login')
            # elif request.path.startswith('/admin/'):
            #     return HttpResponseForbidden("Anda Tidak Punya Akses Untuk Mengakses Halaman Ini!")
            
        else:
            if request.path.startswith('/auth/') and request.user.role != 'buyer' and not request.user.no_telp == '+6285210000000':
                return redirect('seller_dashboard')
            elif request.path.startswith('/auth/') and request.user.role != 'seller' and not request.user.no_telp == '+6285210000000':
                return redirect('home')
            elif request.path.startswith('/pembeli/') and request.user.role != 'buyer' and not request.user.no_telp == '+6285210000000':
                return redirect('seller_dashboard')
            elif request.path.startswith('/penjual/') and request.user.role != 'seller' and not request.user.no_telp == '+6285210000000':
                return redirect('home')
            elif request.path.startswith('/admin/') and request.user.role != 'admin':
                return HttpResponseForbidden("Anda Tidak Punya Akses Untuk Mengakses Halaman Ini!")
        
        return self.get_response(request)
    

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user.is_authenticated and request.user.no_telp == '+6285210000000' and request.user.role == 'buyer' and not request.path.startswith('/auth/complete_profile/'):
                return redirect('complete_profile')

        response = self.get_response(request)
        return response