
from django.shortcuts import render, redirect
from django.utils.text import slugify

from django.views import View
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from .serializers import ProductSerializer
from .models import Product
from .forms import ProductCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views import generic

from .filters import ProductsFilter

class ProductRetrieveListApi(
        LoginRequiredMixin,
        ListAPIView,
        View):
    queryset = Product.get_all_products()
    serializer_class = ProductSerializer
    

    def get(self, request, *args, **kwargs):
        self.request = request
        products = self.get_queryset()
        
        product_filter = ProductsFilter(request.GET, queryset=self.get_queryset())
        products = product_filter.qs
        
        context = {'products': products, 'filter': product_filter}
        return render(request, 'products/index.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CreateProductView(
                LoginRequiredMixin,
                CreateView):
    model = Product
    template_name = "products/product_create.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:products')
    
    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.slug = product.set_default_slug
            product.save()
            
            messages.success(request, 'The product was successfully created!')
            return redirect(self.success_url)
        
        messages.error(self.request, 'Invalid data!')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)
    

class UpdateProductView(LoginRequiredMixin,
                        UpdateView):
    
    template_name = 'products/product_update.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:products')
    context_object_name = 'product'
    
    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(instance=self.get_object())
        if form.is_valid():
            product = form.save(commit=False)
            product.slug = product.set_default_slug
            product.save()
            
            messages.success(request, 'Successfully updated!')
            return redirect(self.success_url)
        
        messages.error(self.request, 'Invalid data!')
        return super().post(request, *args, **kwargs)
        
    def get_object(self):
        product = Product.objects.get(slug=self.kwargs['slug'])
        return product

    def get(self, request, *args, **kwargs):
        context = {}
        context["form"] = ProductCreateForm(instance=self.get_object())
        return render(request, self.template_name, context)


class DeleteProductView(LoginRequiredMixin, 
                        DeleteView):

        success_url = reverse_lazy('products:products')
        context_object_name = 'product'
        
        def get_object(self):
            product = Product.objects.get(slug=self.kwargs['slug'])
            return product
        
        def delete(self, request, *args, **kwargs):
            if self.get_queryset:
                messages.success(request, 'Product deleted successfully!')
                
            messages.success(request, 'Product does not exist!')
            return super().delete(request, *args, **kwargs)


class DetailProductView(LoginRequiredMixin, 
                        DetailView):
    context_object_name = 'product'
    
    def get_object(self):
        product = Product.objects.get(slug=self.kwargs['slug'])
        return product
    
    
    
    
    

        
            
        
        
