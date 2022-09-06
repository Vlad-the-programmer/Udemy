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

from .models import Customer, Profile
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from django.http.response import Http404


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'auth/register/register.html'
    # redirect_authenticated_user = True
    
    def form_valid(self, form):
        
        email = request.POST['email']
        if Customer.get_customer_by_email(email=email) == False:
            if form.is_valid():
                form.save()
                account = authenticate(request, 
                                    username=email,
                                    password=request.POST['password'])
                
                login(request, account)
                messages.success(request, 'The account was successfully created!!!')
                
            return redirect(reverse_lazy('register'))
    
        return redirect(reverse_lazy('login'))


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = self.get_form_class()
        context['user'] = self.request.user
        return context


def logout(request):
    return logout_then_login(request, login_url='login/')

@csrf_exempt
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
                
                user.username = user.username.lower()
                user.save()
                
                login(request, user, 
                    backend='allauth.account.auth_backends.AuthenticationBackend')
                
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
    return render(request, 'login/login.html', context)


class ProfileDetailView(LoginRequiredMixin,
                        DetailView):
    
    context_object_name = 'profile'
    template_name = 'auth/profile_detail.html'
    model = Profile
    
    def get_object(self):
        customer = Customer.objects.get(customer_id=self.kwargs['pk'])
        return customer.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        customer = Customer.objects.get(customer_id=self.kwargs['pk'])
        context['customer'] = customer.profile
        return context
    
   
    

class UpdateProfileView(LoginRequiredMixin,
                        UpdateView):
    
    template_name = 'auth/profile_update.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('user-auth:profile-detail')
    model = Profile
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileUpdateForm(instance=profile)
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                if not Customer.objects.filter(profile=profile).first():
                    form.save()
                
                messages.success(request, 'Successfully updated!')
                return redirect(self.success_url)
        
            messages.error(request, 'Invalid data!')
            return super().post(request, *args, **kwargs)
        
    def get_object(self):
        customer = Customer.objects.get(customer_id=self.kwargs['pk'])
        return customer.profile

    def get(self, request, *args, **kwargs):
        context = {}
        context["form"] = ProfileUpdateForm(instance=self.get_object())
        # context['profile'] = self.get_object()
        context['user'] = request.user
        return render(request, self.template_name, context)


class DeleteProfileView(LoginRequiredMixin, 
                        DeleteView):

        success_url = reverse_lazy('user-auth:profile-detail')
        context_object_name = 'profile'
        template_name = 'auth/profile_confirm_delete.html'
        model = Profile
        
        
        def post(self, request, *args, **kwargs):
            self.request = request
            
            if self.get_queryset:
                messages.success(request, 'Profile deleted successfully!')
                
            messages.success(request, 'Profile does not exist!')
            return super().post(request, *args, **kwargs)

        def get_object(self):
            customer = Customer.objects.get(customer_id=self.kwargs['pk'])
            return customer.profile
        # def get_object(self):
        #     try:
        #         profile = Profile.objects.get(profile_id=self.kwargs['pk'])
        #     except:
        #         return Http404
        
        #         print(profile.profile_id)
        #         return profile