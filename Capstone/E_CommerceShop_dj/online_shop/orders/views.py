import json
from django.shortcuts import render, redirect
from django.views.generic.edit import (CreateView,
                                       FormView,
                                       UpdateView,
                                       DeleteView
                                       )
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy

from user_auth.models import Profile
from products.models import Product
from .forms import OrderCreateForm, OrderUpdateForm
from .models import Order, OrderItem
from .utils import cartData, cookieCart, guestOrder


class CartView(TemplateView):
    template_name = 'auth/profile_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        try:
            data = cartData(self.request)
            # cartItems = data['cartItems']
            order = data['order']
            # items = data['items']
        except:
            order = None
            # items = None
            # cartItems = 0
        context['order'] = order
        return context


class CookieCartView(TemplateView):
    template_name = 'orders/cookie-cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            data = cartData(self.request)
            # cartItems = data['cartItems']
            order = data['order']
            # items = data['items']
        except:
            order = None
            items = None
            cartItems = 0
            
        context['order'] = order
        # context['items'] = items
        # context['cartItems'] = cartItems
        return context
    
class OrderCreateView(LoginRequiredMixin,
                      CreateView):
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy("products:products")

    def form_valid(self, form):
        order = form.save(commit=False)
        order.slug = order.set_default_slug
        order.customer = self.request.user
        order.save()
        
        messages.success(self.request, 'The order was successfully created!')
        return redirect(self.success_url)
           

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(product_id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, item_created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
        
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


class OrderDetailView(LoginRequiredMixin,
                      DetailView):
    
    template_name = "orders/order_detail.html"
    context_object_name = 'order'
    
    def get_object(self):
        customer = self.request.user
        order = Order.objects.get(customer=customer, transaction_id=self.kwargs["transaction_id"])
        return order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user)
        return context
    
    
class OrderDeleteView(LoginRequiredMixin,
                      DeleteView):
    
    context_object_name = 'order'
    success_url = reverse_lazy("orders:orders")
    template_name = "orders/order_confirm_delete.html"
        
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
        
            
def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)        
        