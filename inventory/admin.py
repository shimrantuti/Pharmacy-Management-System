from django.contrib import admin
from . import models
from  inventory.models import Medicine
from  inventory.models import Category
from  inventory.models import Supplier
from  inventory.models import Batch
from  inventory.models import PurchaseOrder
from  inventory.models import Order
from  inventory.models import OrderItem


# Register your models here.

#   APPLY INLINE PROPERTY IN INVENTORY


class BatchInline(admin.TabularInline):
    model=Batch
    fields=['batch_no','manufacture_date','expiry_date','initial_quantity','current_quantity','medicine','purchase_price','mrp','purchaseOrder']

@admin.register(Medicine)   
class MedicineAdmin(admin.ModelAdmin):
    list_display=('medicine_name','generic_name','description','category')
    # inlines=[BatchInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','description')
admin.site.register(Category,CategoryAdmin)     

class SupplierAdmin(admin.ModelAdmin):
    list_display=('sup_name','contact_person','email','address','gst_number')
admin.site.register(Supplier,SupplierAdmin)     

class BatchAdmin(admin.ModelAdmin):   
    list_display=('batch_no','manufacture_date','expiry_date','initial_quantity','current_quantity','medicine','purchase_price','mrp','purchaseOrder')
    search_fields=['medicine__medicine_name','batch_no']
  
admin.site.register(Batch,BatchAdmin)  

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display=('purchase_date','supplier','total_amount')
    inlines=[BatchInline]

admin.site.register(PurchaseOrder,PurchaseOrderAdmin) 



        #   APPLING Sales INLINE PROPERTY


class OrderItemInline(admin.TabularInline):
    model=OrderItem
    autocomplete_fields=['batch']
    fields=['batch','quantity','price_at_sale']
    readonly_fields=['price_at_sale']
    extra=1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['customer_name','phone_no','timestamp','total_amount']
    readonly_fields=['total_amount']
    inlines=[OrderItemInline]



          
