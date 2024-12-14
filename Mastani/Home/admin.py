from django.contrib import admin
from .models import literasi, ContactMessage

# Admin untuk model literasi
class literasi_admin(admin.ModelAdmin):
    # Hanya tampilkan atribut yang ada dalam model literasi
    list_display = ('title', 'deskripsi', 'author', 'created_date', 'link_literasi', 'img', 'img_preview')
    search_fields = ('title', 'author')  # Sesuaikan dengan atribut yang ada di model literasi
    
    def img_preview(self, obj):
        if obj.img:
            return f'<img src="{obj.img.url}" style="max-width: 100px;"/>'
        return "tidak ada gambar"
    
    img_preview.allow_tags = True
    img_preview.short_description = "Preview gambar"

# Admin untuk model ContactMessage
class ContactMessageAdmin(admin.ModelAdmin):
    # Tampilkan atribut yang ada di model ContactMessage
    list_display = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email')

# Daftarkan model dengan admin yang sesuai
admin.site.register(literasi, literasi_admin)
admin.site.register(ContactMessage, ContactMessageAdmin)
