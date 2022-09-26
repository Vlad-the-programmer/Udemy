from django.shortcuts import render, redirect
from django.views.generic.edit import (CreateView,
                                       FormView,
                                       UpdateView,
                                       DeleteView
                                       )
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Order
from .forms import OrderCreateForm, OrderUpdateForm
from user_auth.models import Profile

class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    
    def get_object(self):
        orders = Order.objects.filter(customer=self.request.user).order_by("-date_created")
        return orders
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_object()
        context["products"] = [order.products.all() for order in orders]
        return context
    
    
class OrderCreateView(LoginRequiredMixin,
                      CreateView):
    model = Order
    form_class = OrderCreateForm
    context_object_name = 'order'
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy("orders:orders")

    def form_valid(self, form):
        order = form.save(commit=False)
        order.slug = order.set_default_slug
        order.customer = self.request.user
        order.save()
        
        messages.success(self.request, 'The order was successfully created!')
        return redirect(self.success_url)
           
class OrderUpdateView(LoginRequiredMixin,
                      UpdateView):
    form_class = OrderUpdateForm
    template_name = 'orders/order_list.html'
    
    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, message="Order updated!")
        return super().form_valid(form)
    
    def get_object(self):
        order = Order.objects.get(slug=self.kwargs['slug'])
        return order
    
    def get_success_url(self):
        order = self.get_object()
        
        success_url = reverse_lazy("orders:order-detail", 
                                        kwargs={"slug": order.slug})
        return success_url
    
class OrderDetailView(LoginRequiredMixin,
                      DetailView):
    
    template_name = "orders/order_detail.html"
    context_object_name = 'order'
    
    def get_object(self):
        order = Order.objects.get(slug=self.kwargs['slug'])
        return order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user)
        products = []
        for order in orders:
            for product in order.products.all():
                products.append(product)
        context["orders"] = orders
        context["profile"] =  Profile.objects.filter(user=self.request.user)
        context["products"] = products
        
        return context
    
    
class OrderDeleteView(LoginRequiredMixin,
                      DeleteView):
    
    context_object_name = 'order'
    success_url = reverse_lazy("orders:orders")
        
    def get_object(self):
        order = Order.objects.get(slug=self.kwargs['slug'])
        return order
    
    def delete(self, request):
        order = self.get_object()
        if order:
            messages.add_message(request, messages.SUCCESS, "Deleted!")
            order.delete(self)
        else:
            messages.add_message(request, messages.ERROR, "The order does not exist!")
        
        return super().delete(request)
            
        
    
        
        