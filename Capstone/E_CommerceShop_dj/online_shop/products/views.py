
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from .models import Product, Category
from .serializers import ProductSerializer
from .forms import ProductCreateForm, CustomerCreateForm, OrderCreateForm, SignUpForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import authenticate, login, logout
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


class SignUpView(LoginRequiredMixin, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'products/register/register.html'
    

    def post(self, request, *args, **kwargs):
        
        user = User(username=request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    password=request.POST['password'])
        if user is not None:
            user.save()
            return redirect('login')
        else:
            return redirect('register')

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['form'] = SignUpForm()
        context['user'] = self.request.user
        return context

class LoginView(LoginView):
    form_class = LoginForm()
    success_url = reverse_lazy('products')
    template_name = 'products/login/login.html'

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['form'] = LoginForm()
        context['user'] = self.request.user
        
        return context

    def form_valid(self, form):
        user = authenticate(email=form.email.data, password=form.password.data)
        if user is not None:
            login(user)
            return redirect('products')
        else:
            return redirect('login')


# class LogOut(LogoutView):
#     template_name = 'products/index.html'
def logout(request):
    return logout_then_login(request, login_url='login')
    
    
    
    


