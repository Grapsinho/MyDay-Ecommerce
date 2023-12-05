from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin

# Register your models here.

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(ProductInventory)
admin.site.register(ProductType)
admin.site.register(ProductTypeAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Stock)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Costumer)
admin.site.register(ShippingAddress)



# @admin.register(Category, MPTTModelAdmin)
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {
#         "slug": ("name",),
#     }