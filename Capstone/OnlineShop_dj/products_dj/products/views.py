from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import ProductSerializer
from .forms import ProductCreateForm, CustomerCreateForm, OrderCreateForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class ProductRetrieveListApi(ListCreateAPIView, View):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = ProductCreateForm()
        if request.method == 'POST':
            form = ProductCreateForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form': form, 'products': Product.objects.all()}
        return render(request, 'products/index.html', context)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        context = {'products': products}
        return render(request, 'products/index.html', context)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'register/register.html'
    context_object_name = 'form'

