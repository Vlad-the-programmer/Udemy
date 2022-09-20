from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

from .models import Order
from .forms import OrderCreateForm


def index(request):
    return render(request, 'products/index.html')


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'
    
    def form_valid(self, form):
        form.save()
        
        