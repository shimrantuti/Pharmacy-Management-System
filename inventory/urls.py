from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('category',views.CategoryView,basename='category')
router.register('medicine',views.MedicineView,basename='medicine')
router.register('supplier',views.SupplierView,basename='supplier')
router.register('batch',views.BatchView,basename='batch')
router.register('order',views.OrderView,basename='order')
router.register('OrderItem',views.OrderItemView,basename='OrderItem')
urlpatterns=[
   path('',include(router.urls)),
] 