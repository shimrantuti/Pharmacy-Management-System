from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from inventory import serializer
from inventory.serializer import CategorySerializer
from inventory.serializer import MedicineSerializer
from inventory.serializer import SupplierSerializer
from inventory.serializer import BatchSerializer,OrderSerializer,OrderItemSerializer
from inventory.models import Category
from  inventory.models import Medicine
from  inventory.models import Supplier
from  inventory.models import Batch,Order,OrderItem


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

class BatchView(viewsets.ModelViewSet):
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer

class OrderView(viewsets.ModelViewSet):
     queryset=Order.objects.all()
     serializer_class=OrderSerializer  

class OrderItemView(viewsets.ModelViewSet):
     queryset=OrderItem.objects.all()
     serializer_class=OrderItemSerializer                         