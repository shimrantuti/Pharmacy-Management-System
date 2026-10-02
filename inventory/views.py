from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from inventory import serializer
from inventory.serializer import CategorySerializer
from inventory.serializer import MedicineSerializer
from inventory.serializer import SupplierSerializer,PurchaseOrderSerializer,PurchaseInvoiceSerializer
from inventory.serializer import BatchSerializer,OrderSerializer,OrderItemSerializer
from inventory.models import Category
from  inventory.models import Medicine
from  inventory.models import Supplier,PurchaseOrder,PurchaseInvoice
from  inventory.models import Batch,Order,SalesOrderItem,PurchaseInvoice
from rest_framework.permissions import IsAuthenticated
from inventory.permissions import (
    IsAdmin,
    IsAdminOrSellerReadOnly,
    IsAdminOrSellerOrder,
    IsAdminOrSellerOrderItem
)

# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes = [IsAdminOrSellerReadOnly]
     
class MedicineView(viewsets.ModelViewSet):
    queryset=Medicine.objects.all()
    serializer_class=MedicineSerializer
    permission_classes = [IsAdminOrSellerReadOnly]

class SupplierView(viewsets.ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializer
    permission_classes = [IsAdmin]


class PurchaseOrderView(viewsets.ModelViewSet) :
      queryset=PurchaseOrder.objects.all()
      serializer_class=PurchaseOrderSerializer
      permission_classes = [IsAdmin]


class PurchaseInvoiceView(viewsets.ModelViewSet) :
      queryset=PurchaseInvoice.objects.all()
      serializer_class=PurchaseInvoiceSerializer
      permission_classes = [IsAdmin]


class BatchView(viewsets.ModelViewSet):
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer
    permission_classes = [IsAdminOrSellerReadOnly]

class OrderView(viewsets.ModelViewSet):
     queryset=Order.objects.all()
     serializer_class=OrderSerializer  
     permission_classes = [IsAdminOrSellerOrder]

class SalesOrderItemView(viewsets.ModelViewSet):
     queryset=SalesOrderItem.objects.all()
     serializer_class=OrderItemSerializer    
     permission_classes = [IsAdminOrSellerOrderItem]                     

