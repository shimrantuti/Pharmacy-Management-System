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


# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
     
class MedicineView(viewsets.ModelViewSet):
    queryset=Medicine.objects.all()
    serializer_class=MedicineSerializer

class SupplierView(viewsets.ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializer


class PurchaseOrderView(viewsets.ModelViewSet) :
      queryset=PurchaseOrder.objects.all()
      serializer_class=PurchaseOrder


class PurchaseInvoiceView(viewsets.ModelViewSet) :
      queryset=PurchaseInvoice.objects.all()
      serializer_class=PurchaseInvoice



class BatchView(viewsets.ModelViewSet):
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer

class OrderView(viewsets.ModelViewSet):
     queryset=Order.objects.all()
     serializer_class=OrderSerializer  

class SalesOrderItemView(viewsets.ModelViewSet):
     queryset=SalesOrderItem.objects.all()
     serializer_class=OrderItemSerializer                         

class PurchaseInvoiceView(viewsets.ModelViewSet) :
      queryset=PurchaseInvoice.objects.all()
      serializer_class=PurchaseInvoice