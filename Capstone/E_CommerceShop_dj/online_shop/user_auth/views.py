from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views import generic
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Customer, Profile
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from orders.models import Order
from products.models import Product

class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'auth/register/register.html'
    
    def form_valid(self, form):
        
        email = self.request.POST['email']
        if Customer.get_customer_by_email(email=email) == False:
            
                user = form.save(commit=False)
                user.username.lower()
                user.email.lower()
                user.save()
                
                login(
                    self.request,
                    user,
                    backend='allauth.account.auth_backends.AuthenticationBackend'
                    )
                
                messages.success(self.request, 'The account was successfully created!!!')
                return redirect(reverse_lazy('products:products'))
            
        messages.error(self.request, "User with the email already exists. Try to login.")
        return redirect(reverse_lazy('user-auth:login'))


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = self.get_form_class()
        context['user'] = self.request.user
        return context


def logout(request):
    return logout_then_login(request, login_url='login/')

@method_decorator(ensure_csrf_cookie, name='dispatch')
def signup(request):
    if request.method == 'POST':
        
        form = SignUpForm(request.POST or None)
        email = request.POST['email']
        if Customer.get_customer_by_email(email=email) == False:
            if form.is_valid():
                user = form.save(commit=False)
                # account = authenticate(request, 
                #                     username=email,
                #                     password=request.POST['password'])
                
                user.username.lower()
                user.save()
                
                login(
                    request,
                    user, 
                    backend='allauth.account.auth_backends.AuthenticationBackend'
                )
                
                messages.success(request, 'The account was successfully created!!!')
                return redirect(reverse_lazy('products:products'))
            
            messages.error(request, f'{form.errors}') 
            return redirect(reverse_lazy('user-auth:register'))
    
        return redirect(reverse_lazy('user-auth:login'))
    form = SignUpForm()
    context = {'form': form, 'user': request.user}
    return render(request, 'auth/register/register.html', context)


def login_user(request):
    form = LoginForm() 
    
    if request.method == 'POST':
        if form.is_valid():
            form = LoginForm(request.POST)
            user = form.save()
            # user = authenticate(request,
            #                 username=request.POST['email'],
            #                 password=request.POST['password'])
            
            if user is not None:
                login(request, user)
                messages.success(request, f'You have successfully logged in as \
                                {user.get_username}')
            else:
                messages.info(request, 'User does not exist!!! Register, please!')
                return redirect(reverse_lazy('user-auth:register'))
            
        return redirect(reverse_lazy('user-auth:login'))
    context ={'form': form}
    return render(request, 'auth/login/login.html', context)


class ProfileDetailView(LoginRequiredMixin,
                        DetailView):
    
    context_object_name = 'profile'
    template_name = 'auth/profile_detail.html'
    
    def get_object(self):
        profile = Profile.objects.get(profile_id=self.kwargs['pk'])
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['user'] = user
        # context['profile'] = self.get_object()
        context['orders'] = Order.objects.filter(customer=user).order_by('-date_created')
        context['products'] = Product.objects.filter(customer=user).order_by('-date_created')
        return context
    
   
    
class UpdateProfileView(LoginRequiredMixin,
                        UpdateView):
    
    template_name = 'auth/profile_update.html'
    form_class = ProfileUpdateForm
    context_object_name = 'profile'
    
    def get_success_url(self):
            profile = self.get_object()
            success_url = reverse_lazy('user-auth:profile-detail', 
                                   kwargs={'pk': profile.profile_id})
            return success_url
        
    @method_decorator(ensure_csrf_cookie, name='dispatch')
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileUpdateForm(instance=profile)
        # if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if profile:
                form.save()
            
                messages.success(request, 'Successfully updated!')
                return redirect(self.get_success_url())
            
            messages.error(request, 'Profile does not exist!')
            return redirect(reverse_lazy('user-auth:signup'))
            
        messages.error(request, 'Invalid data!')
        return render(request, self.template_name, self.get_context_data())
        
    def get_object(self):
        profile = Profile.objects.get(profile_id=self.kwargs['pk'])
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProfileUpdateForm(instance=self.get_object())
        # context['user'] = self.request.user
        return context
    

class DeleteProfileView(LoginRequiredMixin, 
                        DeleteView):

        context_object_name = 'customer'
        template_name = 'auth/profile_confirm_delete.html'
        
        def get_success_url(self):
            profile = self.get_object()
            success_url = reverse_lazy('user-auth:profile-detail', 
                                   kwargs={'pk': profile.profile_id})
            return success_url
        
        @method_decorator(ensure_csrf_cookie, name='dispatch')
        def post(self, request, *args, **kwargs):
            if self.get_object:
                messages.success(request, 'Profile deleted successfully!')
                
                return super().delete(request, *args, **kwargs)
            
            messages.success(request, 'Profile does not exist!')
            return redirect(reverse_lazy('user-auth:signup'))

        def get_object(self):
            profile = Profile.objects.get(profile_id=self.kwargs['pk'])
            return profile.user
       