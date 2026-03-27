from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

class Medicine(models.Model):
    medicine_name=models.CharField(max_length=200,unique=True)
    generic_name=models.CharField(max_length=200)
    description=models.TextField()
    low_stock_threshold=models.PositiveIntegerField(default = 0)
    category=models.ForeignKey("inventory.Category", on_delete=models.CASCADE)


    @property
    def total_available_stock(self):
        today=timezone.now().date()
        valid_batches = self.batch_set.filter(expiry_date__gt=today)
        total=valid_batches.aggregate(Sum("current_quantity"))["current_quantity__sum"]
        return total or 0
    
    def stock_status(self):
        total=self.total_available_stock
        if total == 0:
            return "❌ Out of Stock"
        
        elif total < self.low_stock_threshold:
            return f"⚠️ Low Stock!! "
        
        return "✅ In Stock"
    
    class Meta:
        verbose_name_plural="Medicines"

    def __str__(self):
        return self.medicine_name

class Supplier(models.Model):
    sup_name=models.CharField(max_length=100,unique=True)
    contact_person=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField(blank=True)
    address=models.TextField()
    gst_number=models.CharField(max_length=15,blank=True)

    class Meta:
        verbose_name_plural = "Suppliers"


    def __str__(self):
        return self.sup_name


class PurchaseOrderItem(models.Model):
    medicine_name = models.CharField(max_length=255)
    quantity_ordered = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') # e.g., Pending, Received

    def __str__(self):
        return f"Order: {self.medicine_name} from {self.supplier.sup_name}"

  #Purchase Detail with Legal Document (Invoice)
class PurchaseDetail(models.Model):
   
    purchase_order_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.CASCADE)
    
    invoice_no = models.CharField(max_length=100, unique=True) # The ID from the paper bill
    received_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_no}"


class Batch(models.Model):
    batch_no = models.CharField(max_length=50, unique=True)
    manufacture_date = models.DateField()  
    expiry_date = models.DateField()  
    initial_quantity = models.IntegerField()
    current_quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicine = models.ForeignKey("Medicine", on_delete=models.PROTECT) 
    purchaseOrder = models.ForeignKey(PurchaseDetail, on_delete=models.CASCADE)

    class Meta:
        ordering = ['expiry_date','batch_no'] # Fixes the Autocomplete requirement
        verbose_name_plural="Batches"


    def __str__(self):
       
        return f"{self.medicine.medicine_name} - {self.batch_no}"
    

class Order(models.Model):
    customer_name=models.CharField(max_length=100,null=False)
    phone_no=models.CharField(max_length=15,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
     

    def update_total_bill(self):
        items=self.orderitem_set.all()
        bill = sum(item.quantity * item.price_at_sale for item in items)
        self.total_amount=bill
        self.save()
    def __str__(self):
        return self.customer_name
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)    
    quantity=models.PositiveIntegerField()
    price_at_sale=models.DecimalField(max_digits=15,decimal_places=2)

    def clean(self):
        if self.pk:
            original_qty= OrderItem.objects.get(pk=self.pk).quantity
        else:
            original_qty=0  

         #calculate change in quantity
        self._delta = self.quantity - original_qty 

        #Prevents sale if requested quantity exceeds  current stock 
        if self._delta > 0 and self._delta > self.batch.current_quantity :
              raise ValidationError(f"Insufficient stock in Batch {self.batch.batch_no}!")
           

    def save(self,*args,**kwargs):

        self.full_clean()

        if self.pk:
            original_qty= OrderItem.objects.get(pk=self.pk).quantity
        else:
            original_qty=0  
            
        #use delta calulate in clean()
        delta=getattr(self,"_delta",None)
    
        #update the stoch in the batch table
        self.batch.current_quantity -= delta

        
        if not self.price_at_sale and self.batch.mrp:
            self.price_at_sale=self.batch.mrp
        self.batch.save()
        super().save(*args,**kwargs)

        #recalculate  the  master order total
        self.order.update_total_bill()    

    def delete(self,*args,**kwargs):
        # Refund the quantity back to the batch when an item is deleted
        self.batch.current_quantity += self.quantity
        self.batch.save()
        
        # 2. Store the order reference BEFORE deleting the item
        order_to_update = self.order
        super().delete(*args,**kwargs)
        #Refresh the bill
        order_to_update.update_total_bill()