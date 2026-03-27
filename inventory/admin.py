from django.contrib import admin
from . import models
from  inventory.models import Medicine , Category ,Supplier ,Batch , Order, OrderItem,PurchaseDetail,PurchaseOrderItem



# Registeration of models 

#   APPLY INLINE PROPERTY IN INVENTORY

class BatchInline(admin.TabularInline):
    model=Batch
    fields=['batch_no','manufacture_date','expiry_date','initial_quantity','current_quantity','medicine','purchase_price','mrp','purchaseOrder']
    autocomplete_fields=['medicine']
    extra=1


@admin.register(Medicine)   
class MedicineAdmin(admin.ModelAdmin):
    list_display=('medicine_name','generic_name','description','low_stock_threshold','category','stock_status','total_available_stock')
    search_fields = ('medicine_name', 'generic_name')
    list_filter = ('category',)
    # inlines=[BatchInline]
    
    #Search field at the top
    search_fields = ('medicine_name', 'generic_name')

    #  Filter sidebar on the right
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','description')
admin.site.register(Category,CategoryAdmin)  


class SupplierAdmin(admin.ModelAdmin):
    list_display=('sup_name','contact_person','email','address','gst_number')
admin.site.register(Supplier,SupplierAdmin)

class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display=('medicine_name','quantity_ordered', 'supplier','order_date','status')
admin.site.register(PurchaseOrderItem,PurchaseOrderItemAdmin)



class PurchaseDetailAdmin(admin.ModelAdmin):
    list_display=('purchase_order_item','invoice_no', 'received_date', 'total_amount')
    inlines= [BatchInline]
admin.site.register(PurchaseDetail,PurchaseDetailAdmin)



class BatchAdmin(admin.ModelAdmin):   
    list_display=('batch_no','manufacture_date','expiry_date','initial_quantity','current_quantity','medicine','purchase_price','mrp','purchaseOrder')
    search_fields=['medicine__medicine_name','batch_no']
  
admin.site.register(Batch,BatchAdmin) 




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



        
