from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('category',views.CategoryView,basename='category')
router.register('medicine',views.MedicineView,basename='medicine')
router.register('supplier',views.SupplierView,basename='supplier')
router.register('purchaseOrder',views.PurchaseOrderView,basename='purchaseOrder')
router.register('purchaseInvoice',views.PurchaseInvoiceView,basename='purchaseInvoice')
router.register('batch',views.BatchView,basename='batch')
router.register('order',views.OrderView,basename='order')
router.register('SalesOrderItem',views.SalesOrderItemView,basename='SalesOrderItem')
urlpatterns=[
   path('',include(router.urls)),
] 