
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from .models import Product, Category, Customer
from .serializers import ProductSerializer
from .forms import ProductCreateForm, CustomerCreateForm, OrderCreateForm, SignUpForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.auth import authenticate, login
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
    form_class = CustomerCreateForm
    success_url = reverse_lazy('login')
    template_name = 'products/register/register.html'
    

    def post(self, request, *args, **kwargs):
        form = CustomerCreateForm(request.POST)
    
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            context = {'user': user}
            
            return render(request, 'products/index.html', context)
       
        return redirect('register')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = CustomerCreateForm
        context['user'] = self.request.user
        return context


# class LoginView(LoginView):
#     form_class = LoginForm
#     success_url = reverse_lazy('products')
#     template_name = 'products/login/login.html'

#     def get_context_data(self, *args, **kwargs):
#         context = {}
#         context['form'] = LoginForm
#         context['user'] = self.request.user
#         return context

#     # def form_valid(self, form):
#     #     form.save()
#     #     user = authenticate(email=form.email.data, password=form.password.data)
#     #     if user is not None:
#     #         login(user)
#     #         return redirect('products')
#     #     return redirect('login')
#     def post(self, request, *args, **kwargs):
#         user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
#         if user is not None:
#             login(request, user)
#             redirect('products')
#         return redirect('register')


# class LogOut(LogoutView):
#     template_name = 'products/index.html'
def logout(request):
    return logout_then_login(request, login_url='login/')
    
    
    
    


