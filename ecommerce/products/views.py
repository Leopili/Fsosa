from django.shortcuts import render
from django.views.generic import ListView, DetailView
from products.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator

class Home(ListView):
    model = Category
    template_name = 'products/home.html'

    

class Productos(ListView):
    model = Product
    template_name = 'products/home2.html'


class ProductDetail(LoginRequiredMixin, DetailView):
	model = Product

def home1(request):
    return render(request, "products/base2.html")

    
class SingleCat(DetailView):
    model = Category
    

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       current_category = context['object']
       context['products'] = current_category.product_set.all()
       return context