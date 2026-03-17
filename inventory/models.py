from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    medicine_name=models.CharField(max_length=200,unique=True)
    generic_name=models.CharField(max_length=200)
    description=models.TextField()
    category=models.ForeignKey("inventory.Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.medicine_name

class Supplier(models.Model):
    sup_name=models.CharField(max_length=100,unique=True)
    contact_person=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField(blank=True)
    address=models.TextField()
    gst_number=models.CharField(max_length=15,blank=True)

    def __str__(self):
        return self.sup_name

class PurchaseOrder(models.Model):
    purchase_date=models.DateField(auto_now_add=True)
    supplier=models.ForeignKey(Supplier,on_delete=models.PROTECT)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.supplier.sup_name}-{self.purchase_date}"


class Batch(models.Model):
    batch_no = models.CharField(max_length=50, unique=True)
    manufacture_date = models.DateField()  
    expiry_date = models.DateField()  
    initial_quantity = models.IntegerField()
    current_quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicine = models.ForeignKey("Medicine", on_delete=models.PROTECT) # Simplified string reference
    purchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)

    class Meta:
        ordering = ['batch_no'] # Fixes the Autocomplete requirement

    def __str__(self):
        # We removed "self.batch.batch_no" which was causing the crash
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
    batch=models.ForeignKey(Batch,on_delete=models.PROTECT)    
    quantity=models.PositiveIntegerField()
    price_at_sale=models.DecimalField(max_digits=15,decimal_places=2)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Store the original quantity to handle stock adjustments during edits
        self._original_qty = self.quantity if self.pk else 0

    def save(self,*args,**kwargs):
        if not self.price_at_sale and self.batch:
            self.price_at_sale=self.batch.mrp
        
        #calcualte change in quantity
        delta = self.quantity - self._original_qty     

        #Prevents sale if requested quantity exceeds  current stock  
        if self.batch.current_quantity < delta:
            raise ValidationError(f"Insufficint stock in Batch {self.batch.batch_no}!")
        
        #update the stoch in the batch table
        self.batch.current_quantity -= delta
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