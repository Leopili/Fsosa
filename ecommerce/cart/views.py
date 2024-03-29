from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Cart, Order
from products.models import Product



# Add to Cart View

def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user
    )
    order_qs = Order.objects.filter(user=request.user, encargado=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{item.name} Cantidad Actualizada.")
            return redirect("mainapp:cart-home")
        else:
            order.orderitems.add(order_item)
            messages.info(request, f"{item.name} Ha sido agregado a su pedido.")
            return redirect("mainapp:cart-home")
    else:
        order = Order.objects.create(
            user=request.user)
        order.orderitems.add(order_item)
        messages.info(request, f"{item.name} Ha sido agregado a su pedido.")
        return redirect("mainapp:cart-home")




# Remove item from cart

def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, item=item)
    if cart_qs.exists():
        cart = cart_qs[0]
        # Checking the cart quantity
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user,
        encargado=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.orderitems.remove(order_item)
            messages.warning(request, "Este artículo ha sido eliminado de su pedido.")
            return redirect("mainapp:home")
        else:
            messages.warning(request, "Este artículo no se encuentra en su pedido")
            return redirect("mainapp:home")
    else:
        messages.warning(request, "No tienes un pedido realizado.")
        return redirect("mainapp:home")


# Cart View

def CartView(request):

    user = request.user

    carts = Cart.objects.filter(user=user, purchased=False)
    orders = Order.objects.filter(user=user, encargado=False)

    if carts.exists():
        if orders.exists():
            order = orders[0]
            return render(request, 'cart/home.html', {"carts": carts, 'order': order})
        else:
            messages.warning(request, "No tienes productos agregados en tu pedido")
            return redirect("mainapp:home")
		
    else:
        messages.warning(request, "No tienes productos agregados en tu pedido")
        return redirect("mainapp:home")



# Decrease the quantity of the cart :

def decreaseCart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        encargado=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitems.filter(item__slug=item.slug).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} Ha sido eliminado de tu pedido.")
            messages.info(request, f"{item.name} Cantidad actualizada.")
            return redirect("mainapp:cart-home")
        else:
            messages.info(request, f"{item.name} Cantidad actualizada.")
            return redirect("mainapp:cart-home")
    else:
        messages.info(request, "No tienen un pedido realizado")
        return redirect("mainapp:cart-home")
