
from django.shortcuts import render, redirect
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

from django.views.generic.edit import CreateView, UpdateView
from django.views import generic

from .filters import ProductsFilter

class ProductRetrieveListApi(
        LoginRequiredMixin,
        ListAPIView,
        View):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # filterset_fields = ['name', 'price']
    # search_fields = ['name', 'price']
    
    @csrf_protect
    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(request.POST, request.FILES)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form': form, 'products': self.get_queryset()}
        return render(request, 'products/index.html', context)

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
                CreateView,
                ):
    model = Product
    template_name = "products/product_create.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy('products')
    
    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The product was successfully created!')
            return redirect(self.success_url)
        
        messages.error(self.request, 'Invalid data!')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)
    

class UpdateProductView(LoginRequiredMixin,
                        UpdateView):
    
    template_name = 'products/update_product.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('products')
    
    
    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(request.POST, request.FILES,
                                 instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated!')
            return redirect(self.success_url)
        
        messages.error(self.request, 'Invalid data!')
        return super().post(request, *args, **kwargs)
        
    def get_object(self, queryset=None):
        object = Product.objects.get(product_id=self.kwargs['pk'])
        return object
        
    
    
    
    

        
            
        
        
