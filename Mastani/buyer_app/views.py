from django.shortcuts import render,redirect
from auth_user.models import CustomUser
from .forms import UpdateUser, TopUpForm
from django.contrib import messages
from .models import TopUp, UserBalance
from django.template.loader import get_template
from .models import TopUp, transfer, IsiPulsa
from xhtml2pdf import pisa
from django.http import HttpResponse

# Create your views here.

def profile_view (request):    
    # update user data

    user_auth = request.user

    if request.method == 'POST':
        form = UpdateUser(request.POST, instance=user_auth)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Anda Telah Di Perbaharui!')
            return redirect('profile_view')
    else:
        form = UpdateUser(instance=user_auth)

    return render(request, "buyer_app/profile.html", {'form':form})


def keuangan_view(request):
    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            nominal = int(form.cleaned_data['nominal'])
            payment_method = form.cleaned_data['payment_method']

            # simpan transaksi ke database
            top_up = TopUp.objects.create(
                user = request.user,
                nominal = nominal,
                payment_method = payment_method,
                status="Berhasil",
            )

            # update saldo user
            user_balance, created = UserBalance.objects.get_or_create(userb=request.user)
            user_balance.balance += nominal
            user_balance.save()

            messages.success(request, f"Isi Saldo Sebesar Rp. {nominal} via {payment_method} berhasil dibuat, Saldo Anda Telah Diperbaharui!")
            return redirect('keuangan_view')
        else:
            messages.error(request, "Form tidak valid. Silahkan Coba Lagi.")
    else:
        form = TopUpForm()

    # Ambil semua data milik user untuk ditampilkan
    data_topUp_terakhir = TopUp.objects.filter(user=request.user).last()
    data_pengeluaran_terakhir = transfer.objects.filter(user=request.user).last()
    data_pengeluaran_terakhir2 = IsiPulsa.objects.filter(user=request.user).last()
    data_topUp = TopUp.objects.filter(user=request.user).order_by('-created_at')
    data_transfer = transfer.objects.filter(user=request.user).order_by('-created_at')
    data_isipulsa = IsiPulsa.objects.filter(user=request.user).order_by('-created_at')

    #ambil total saldo user
    user_balance = UserBalance.objects.filter(userb=request.user).first()
    current_balance = user_balance.balance if user_balance else 0

    return render (request, "buyer_app/keuangan.html", context={'active_page':'keuangan','form':form, 'current_balance':current_balance,'data_topUp_terakhir':data_topUp_terakhir, 'data_topUp':data_topUp, 'data_pengeluaran_terakhir':data_pengeluaran_terakhir, 'data_transfer':data_transfer, 'data_isipulsa':data_isipulsa, 'data_pengeluaran_terakhir2':data_pengeluaran_terakhir2})


def generate_riwayat_pdf (request):
    transaksi = TopUp.objects.filter(user=request.user).order_by('-created_at')
    data_transfers = transfer.objects.filter(user=request.user).order_by('-created_at')
    data_isipulsa = IsiPulsa.objects.filter(user=request.user).order_by('-created_at')
    #load template html
    template = get_template('buyer_app/transaksi.html')
    context = {
        'transaksi':transaksi,
        'user':request.user,
        'data_transfer':data_transfers,
        'data_isipulsa':data_isipulsa,
    }

    html = template.render(context)

    # buat respons PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="riwayat_transaksi.pdf"'

    # ubah html ke pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Terjadi kesalahan saat membuat PDF', status=500)
    
    return response

def transfer_saldo(request):
    if request.method == "POST":
        receiver_phone_num = request.POST.get('receiver_phone')
        amount = request.POST.get('amount')

        # validasi input
        try:
            amount = int(amount)
            if amount <=0:
                messages.error(request, "Nominal Transfer tidak valid (tidak boleh 0).")
                return redirect("keuangan_view")
        except ValueError:
            messages.error(request, "Nominal harus berupa angka.")
            return redirect("keuangan_view")
        
        try:
            receiver = CustomUser.objects.get(no_telp=receiver_phone_num)
        except CustomUser.DoesNotExist:
            messages.error(request, "Nomor Telepon tujuan tidak dapat ditemukan.")
            return redirect('keuangan_view')
        
        #validasi saldo
        try:
            sender_balance = request.user.userbalance
            receiver_balance = receiver.userbalance
        except UserBalance.DoesNotExist:
            messages.error(request, "Kesalahan pada sistem saldo")
            return redirect('keuangan_view')
        
        if sender_balance.balance < amount:
            messages.error(request, "Saldo anda tidak mencukupi.")
            return redirect('keuangan_view')
        
        #proses transfer
        sender_balance.balance -= amount
        sender_balance.save()
        receiver_balance = UserBalance.objects.get(userb=receiver)
        receiver_balance.balance += amount
        receiver_balance.save()

        #simpan transaksi pengirim
        transfer.objects.create(
            user=request.user,
            amount=amount,
            is_sender=True,
            receiver_phone_number=receiver_phone_num,
            status="Berhasil"
        )

        #simpan transaksi penerima
        transfer.objects.create(
            user=receiver,
            amount=amount,
            sender=request.user,  # Tambahkan pengirim
            is_sender=False,
            receiver_phone_number=request.user.no_telp,
            status="Diterima"
        )

        messages.success(request, f"Transfer berhasil ke {receiver.username} sebesar Rp {amount}")
        return redirect('keuangan_view')
    
def isi_pulsa (request):
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        nominal = request.POST.get('nominal')

        # validasi input
        try:
            nominal = int(nominal)
            if nominal <= 0:
                messages.error(request, "Nominal Pulsa tidak valid (Tidak boleh 0).")
                return redirect("keuangan_view")
        except ValueError:
            messages.error(request, "Nominal harus berupa angka")

        #validasi saldo
        user_balance = request.user.userbalance
        if user_balance.balance < nominal:
            messages.error(request, "Saldo anda tidak mencukupi, silahkan isi saldo terlebih dahulu")
            return redirect("keuangan_view")
        
        # Proses transaksi
        user_balance.balance -= nominal
        user_balance.save()

        IsiPulsa.objects.create(
            user=request.user,
            phone_number=phone_number,
            nominal=nominal,
            status="Berhasil",
        )

        messages.success(request, f"Pulsa sebesar Rp {nominal} berhasil dikirim ke nomor {phone_number}")
        return redirect('keuangan_view')
