from django.urls import path 
from . views import checkout,charge, oderView, OrderList, CartView

app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
	path('charge/', charge, name="charge"),
	path('my-orders/', oderView, name="oderView"),
	path('listado_pedido', OrderList.as_view(), name="orderlist"),
	path('pedido/<username>',CartView, name='order_listar'),    
]