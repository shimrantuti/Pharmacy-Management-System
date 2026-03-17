from rest_framework import serializers
from inventory.models import Category
from  inventory.models import Medicine
from  inventory.models import Supplier
from  inventory.models import Batch,PurchaseOrder,Order,OrderItem

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
class BatchSerializer(serializers.ModelSerializer):
    medicine=serializers.StringRelatedField()
    supplier=serializers.StringRelatedField()
    class Meta:
        model=Batch
        fields = "__all__" 

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields = "__all__"                           

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = "__all__"   

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields = "__all__"                                                                   