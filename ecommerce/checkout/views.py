import uuid
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.generic.list import ListView

def checkout(request):	
	
	order_qs = Order.objects.filter(user= request.user, encargado=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals() 
	context = {"order_items": order_items, "order_total": order_total}				
	return render(request, 'checkout/index.html', context)


def charge(request):
	return render (request, 'checkout/charge.html')



def oderView(request):

	try:
		orders = Order.objects.filter(encargado=False)
		context = {
			"orders": orders
		}
	except:
		messages.warning(request, "No hay pedidos realizados")
		return redirect('/')
	return render(request, 'checkout/order.html', context)

class OrderList(ListView):
	model = Order
	template_name = 'checkout/order_list.html'
	queryset = model.objects.filter(encargado=False)

def OrderDetail(request, username):
    order = get_object_or_404(Order, user__username=username)
    context = {'order': order}
    return render(request, 'checkout/order_detail.html' , context )


def CartView(request, username):

    carts = Cart.objects.filter(user__username=username, purchased=False)
    orders = Order.objects.filter(user__username=username, encargado=False)

    if carts.exists():
        if orders.exists():
            order = orders[0]
            return render(request, 'checkout/order_detail.html', {"carts": carts, "order": order})
        else:
            messages.warning(request, "No tienes productos agregados en tu pedido")
            return redirect("mainapp:home")
		
    else:
        messages.warning(request, "No tienes productos agregados en tu pedido")
        return redirect("mainapp:home")