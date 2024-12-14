from django.shortcuts import render,redirect
from auth_user.forms import CustomUserRegistForm, ProfileForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from auth_user.models import CustomUser
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            user = None
            form.add_error(None, 'Email tidak terdaftar.')

        if user is not None:
            if user.check_password(password):
                if user.is_active:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    if user.role == 'seller':
                        return redirect('seller_dashboard')
                    elif user.role == 'admin':
                        role_admin = request.POST.set('admin')
                        print(role_admin)
                        return redirect('/admin')
                    else:
                        return redirect('home')
                else:
                    form.add_error(None, 'Akun tidak aktid (dibanned)')
    else:
        form = AuthenticationForm()

    return render(request, 'auth_user/login.html', context={'form':form})

def register_view(request):

    if request.method == 'POST':
        form = CustomUserRegistForm(request.POST)

        if not form.is_valid():
            print(f"form error: {form.errors}")
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role')
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)

            if user.role == 'seller':
                return redirect('seller_dashboard')
            elif user.role == 'admin':
                return redirect('/admin')
            else:
                return redirect('home')
    else:
        form = CustomUserRegistForm()

    return render(request, 'auth_user/register.html', context={'form':form})

def logout_view (request):
    messages.success(request, "Anda Berhasil Logout!")
    logout(request)
    return redirect('login')

def role_based_redirect(request):
    user = request.user
    if user.is_authenticated:
        if user.role == 'seller':
            return redirect('seller_dashboard')
        elif user.role == 'buyer':
            return redirect('home')
        elif user.role == 'admin':
            return redirect('/admin/')
    return redirect('login')  # Fallback jika tidak ada role

def complete_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)
            if user.role == 'seller':
                return redirect('seller_dashboard')
            elif user.role == 'admin':
                return redirect('/admin')
            else:
                return redirect('home')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'auth_user/complete_profile.html', {'form': form})

