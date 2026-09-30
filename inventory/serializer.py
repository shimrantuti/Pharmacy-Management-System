from rest_framework import serializers
from inventory.models import Category
from  inventory.models import Medicine
from  inventory.models import Supplier,PurchaseOrder
from  inventory.models import Batch,Order,SalesOrderItem,PurchaseInvoice

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = "__all__"   

class MedicineSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    class Meta:
        model=Medicine
        fields = "__all__"  
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields = "__all__" 

class PurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =PurchaseOrder    
        fields= "__all__"                                                                 



class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =PurchaseInvoice    
        fields= "__all__"                                                                         


class BatchSerializer(serializers.ModelSerializer):
    medicine=serializers.StringRelatedField()
    supplier=serializers.StringRelatedField()
    class Meta:
        model=Batch
        fields = "__all__"                     

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = "__all__"  
    def validate(self, attrs):
        if self.instance:
            if "customer_name" in attrs or "phone_no" in attrs:
                raise serializers.ValidationError(
                    "Customer name and phone number cannot be changed after order creation."
                )
        return attrs 

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=SalesOrderItem
        fields = "__all__"    

