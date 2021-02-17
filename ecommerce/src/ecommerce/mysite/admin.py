from django.contrib import admin

# Register your models here.
from .models import Product
from .models import GuestEmail
class ProductAdmin(admin.ModelAdmin):
    list_display=['__str__','slug']
    class Meta:
        model=Product
admin.site.register(Product,ProductAdmin)
admin.site.register(GuestEmail)
