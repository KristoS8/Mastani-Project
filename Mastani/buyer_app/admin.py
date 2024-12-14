from django.contrib import admin
from .models import TopUp, UserBalance, transfer, IsiPulsa
from django.utils.timezone import localtime
from django.utils.html import format_html

# Register your models here.

class TopUpAdmin(admin.ModelAdmin):
    list_display = ('user','nominal','payment_method','status','formatted_created_at')
    readonly_fields = ('formatted_created_at',)

    def formatted_created_at(self,obj):
        waktu_wib = localtime(obj.created_at)
        return format_html(
            '<span>{}</span>',
            waktu_wib.strftime('%d %B %Y, %H:%M WIB')
        )
    formatted_created_at.short_description = 'Tanggal dan Waktu (WIB)'

class TransferAdmin (admin.ModelAdmin):
    list_display = ('user', 'amount','created_at','receiver_phone_number','status')
    readonly_fields = ('formatted_created_at',)

    def formatted_created_at(self,obj):
        waktu_wib = localtime(obj.created_at)
        return format_html(
            '<span>{}</span>',
            waktu_wib.strftime('%d %B %Y, %H:%M WIB')
        )
    formatted_created_at.short_description = 'Tanggal dan Waktu (WIB)'

class IsiPulsaAdmin (admin.ModelAdmin):
    list_display = ('user','phone_number','nominal','created_at')
    readonly_fields = ('formatted_created_at',)

    def formatted_created_at(self,obj):
        waktu_wib = localtime(obj.created_at)
        return format_html(
            '<span>{}</span>',
            waktu_wib.strftime('%d %B %Y, %H:%M WIB')
        )
    formatted_created_at.short_description = 'Tanggal dan Waktu (WIB)'


admin.site.register(TopUp, TopUpAdmin)
admin.site.register(UserBalance)
admin.site.register(transfer, TransferAdmin)
admin.site.register(IsiPulsa, IsiPulsaAdmin)