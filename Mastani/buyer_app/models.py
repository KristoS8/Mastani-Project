from django.db import models
from auth_user.models import CustomUser
from django.utils.timezone import localtime

# Create your models here.

class TopUp (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nominal = models.PositiveIntegerField(default=0)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="Menunggu")
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_created_at(self):
        """Return formatted date and time in Indonesian format."""
        waktu_wib = localtime(self.created_at)
        return waktu_wib.strftime('%d %B %Y, %H:%M WIB')

    def __str__(self):
        return f"Top up {self.nominal} via {self.payment_method} by {self.user.username}"
    

class UserBalance(models.Model):
    userb = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.userb.username} - {self.balance}"
    
class transfer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_transfers')  # Pengirim
    created_at = models.DateTimeField(auto_now_add=True)
    is_sender = models.BooleanField(default=True)  # True untuk pengirim, False untuk penerima
    receiver_phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default="Menunggu")

    def formatted_created_at(self):
        waktu_wib = localtime(self.created_at)
        return waktu_wib.strftime('%d %B %Y, %H:%M WIB')
    
    def __str__(self):
        if self.is_sender:
            return f"Transfer sebanyak {self.amount} ke {self.receiver_phone_number} dari user {self.user} {self.status}"
        else:
            return f"Saldo bertambah sebanyak {self.amount} dari {self.sender}"
    
class IsiPulsa (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    nominal = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default="Menunggu")
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_created_at(self):
        waktu_wib = localtime(self.created_at)
        return waktu_wib.strftime('%d %B %Y, %H:%M WIB')
    
    def __str__(self):
        return f"Pulsa {self.nominal} untuk {self.phone_number} oleh {self.user.username}"