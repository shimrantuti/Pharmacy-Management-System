from django.db import models 
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum , F
from django.db import transaction
import logging


class Category(models.Model):
    category_name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
    

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
    phone_no=models.CharField(max_length=15)
    email=models.EmailField(blank=True)
    address=models.TextField()
    gst_number=models.CharField(max_length=15,blank=True)

    class Meta:
        verbose_name_plural = "Suppliers"


    def __str__(self):
        return self.sup_name


class PurchaseOrder(models.Model):
    medicine_name = models.CharField(max_length=255)
    quantity_ordered = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') # e.g., Pending, Received

    def __str__(self):
        return f"Order: {self.medicine_name} from {self.supplier.sup_name}"

  #Purchase Detail with Legal Document (Invoice)
class PurchaseInvoice(models.Model):
   
    purchase_order_item = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    
    invoice_no = models.CharField(max_length=100, unique=True) # The ID from the paper bill
    received_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_no}"


class Batch(models.Model):
    batch_no = models.CharField(max_length=50, unique=True)
    manufacture_date = models.DateField()  
    expiry_date = models.DateField()  
    initial_quantity = models.PositiveIntegerField()
    current_quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicine = models.ForeignKey("Medicine", on_delete=models.PROTECT) 
    purchaseOrder = models.ForeignKey("PurchaseInvoice", on_delete=models.CASCADE)

    class Meta:

        constraints = [
            models.CheckConstraint(
                check = models.Q(current_quantity__gte = 0),
                name = "batch_current_quantity_not_negative"
            )
        ]
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
    


logger = logging.getLogger(__name__)


class SalesOrderItem(models.Model):

    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items'
    )

    batch = models.ForeignKey(
        'Batch',
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    price_at_sale = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    # =========================================
    # VALIDATION
    # =========================================
    def clean(self):

        errors = {}

        if not self.order_id:
            errors["order"] = "Order is required."

        if not self.batch_id:
            errors["batch"] = "Batch is required."

        if self.quantity is None or self.quantity <= 0:
            errors["quantity"] = (
                "Quantity must be greater than 0."
            )

        if errors:
            raise ValidationError(errors)

    # =========================================
    # STOCK HELPERS
    # =========================================
    @staticmethod
    def increase_stock(batch_id, qty):

        if qty > 0:
            Batch.objects.filter(
                pk=batch_id
            ).update(
                current_quantity=F("current_quantity") + qty
            )

<<<<<<< HEAD
    def delete(self,*args,**kwargs):
        # Refund the quantity back to the batch when an item is deleted
        self.batch.current_quantity += self.quantity
        self.batch.save()
        
        # 2. Store the order reference BEFORE deleting the item
        order_to_update = self.order
        super().delete(*args,**kwargs)
        #Refresh the bill
        order_to_update.update_total_bill()
=======
    @staticmethod
    def decrease_stock(batch_id, qty):

        if qty > 0:
            Batch.objects.filter(
                pk=batch_id
            ).update(
                current_quantity=F("current_quantity") - qty
            )

    # =========================================
    # SAVE
    # =========================================
    def save(self, *args, **kwargs):

        try:

            self.full_clean()

            with transaction.atomic():

                is_update = self.pk is not None

                old_batch_id = None
                old_quantity = 0

                # =============================
                # UPDATE CASE
                # =============================
                if is_update:

                    old_item = (
                        SalesOrderItem.objects
                        .select_for_update()
                        .get(pk=self.pk)
                    )

                    old_batch_id = old_item.batch_id
                    old_quantity = old_item.quantity

                    # Deadlock-safe lock ordering
                    batch_ids = sorted(
                        {
                            old_batch_id,
                            self.batch_id
                        }
                    )

                    locked_batches = (
                        Batch.objects
                        .select_for_update()
                        .filter(pk__in=batch_ids)
                    )

                    batch_map = {
                        batch.pk: batch
                        for batch in locked_batches
                    }

                    current_batch = (
                        batch_map[self.batch_id]
                    )

                    # Same batch update

                    if old_batch_id == self.batch_id:

                        available_stock = (
                            current_batch.current_quantity
                            + old_quantity
                        )

                        if self.quantity > available_stock:
                            raise ValidationError({
                                "quantity":
                                f"Only {available_stock} items available."
                            })

                    # Batch changed

                    else:

                        if (
                            self.quantity >
                            current_batch.current_quantity
                        ):
                            raise ValidationError({
                                "quantity":
                                f"Only {current_batch.current_quantity} items available in new batch."
                            })

                # =============================
                # CREATE CASE
                # =============================
                else:

                    current_batch = (
                        Batch.objects
                        .select_for_update()
                        .get(pk=self.batch_id)
                    )

                    if (
                        self.quantity >
                        current_batch.current_quantity
                    ):
                        raise ValidationError({
                            "quantity":
                            f"Only {current_batch.current_quantity} items available."
                        })

                # =============================
                # HISTORICAL PRICING
                # =============================
                if self.price_at_sale is None:
                    self.price_at_sale = (
                        current_batch.mrp
                    )

                # =============================
                # SAVE MAIN OBJECT FIRST
                # =============================
                super().save(*args, **kwargs)

                # =============================
                # STOCK UPDATE
                # =============================

                if is_update:

                    # SAME BATCH
                    if old_batch_id == self.batch_id:

                        delta = (
                            self.quantity -
                            old_quantity
                        )

                        if delta > 0:

                            self.decrease_stock(
                                current_batch.pk,
                                delta
                            )

                        elif delta < 0:

                            self.increase_stock(
                                current_batch.pk,
                                abs(delta)
                            )

                    # BATCH CHANGED
                    else:

                        self.increase_stock(
                            old_batch_id,
                            old_quantity
                        )

                        self.decrease_stock(
                            current_batch.pk,
                            self.quantity
                        )

                # CREATE
                else:

                    self.decrease_stock(
                        current_batch.pk,
                        self.quantity
                    )

                # =============================
                # UPDATE ORDER TOTAL
                # =============================
                self.order.update_total_bill()

        except ValidationError:
            raise

        except Exception:

            logger.exception(
                f"Error saving SalesOrderItem "
                f"(PK={self.pk})"
            )

            raise

    # =========================================
    # DELETE
    # =========================================
    def delete(self, *args, **kwargs):

        try:

            with transaction.atomic():

                batch = (
                    Batch.objects
                    .select_for_update()
                    .get(pk=self.batch_id)
                )

                order = self.order

                # Restore stock
                self.increase_stock(
                    batch.pk,
                    self.quantity
                )

                # Delete row
                super().delete(*args, **kwargs)

                # Update bill
                order.update_total_bill()

        except Exception:

            logger.exception(
                f"Error deleting SalesOrderItem "
                f"(PK={self.pk})"
            )

            raise
>>>>>>> 392bc24 (Refactor(models): optimize stock deduction architecture in SalesOrderItem)
