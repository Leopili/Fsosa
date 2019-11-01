from django.urls import path, re_path
from cart.views import add_to_cart, remove_from_cart, CartView, decreaseCart
from .views import Home, home1,  ProductDetail, Productos, SingleCat

app_name="mainapp"
urlpatterns = [
    path('inicio', Home.as_view(), name='home'),
    path('', home1, name='inicio'),
    path('product/<slug>/', ProductDetail.as_view(), name='product'),
    path('cart/', CartView, name='cart-home'),
    path('cart/<slug>', add_to_cart, name='cart'),
    path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
    path('remove/<slug>', remove_from_cart, name='remove-cart'),
    re_path(r'^(?P<pk>\d+)$', SingleCat.as_view(), name='category_details'),
]	