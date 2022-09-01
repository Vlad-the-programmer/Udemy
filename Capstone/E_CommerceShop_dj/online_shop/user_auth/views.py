from django.shortcuts import render, redirect
from django.views import View
from .models import Customer
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import CreateView, FormView
from django.views import generic


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'register/register.html'
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

@csrf_protect
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
                return redirect(reverse_lazy('products'))
            messages.error(request, f'{form.errors}') 
            # print(form.errors.as_json())  
            return redirect(reverse_lazy('register'))
    
        return redirect(reverse_lazy('login'))
    form = SignUpForm()
    context = {'form': form}
    return render(request, 'register/register.html', context)


def login_user(request):
    
    if request.method == 'POST':
        if form.is_valid():
            form = LoginForm(request.POST)
            user = authenticate(request,
                            username=form.changed_data['email'],
                            password=form.cleaned_data['password'])
            
            if user is not None:
                login(request, user)
                messages.success(request, f'You have successfully logged in as \
                                {user.get_username}')
            else:
                messages.info(request, 'User does not exist!!! Register, please!')
                return redirect(reverse_lazy('register'))
        else:
            form = LoginForm() 
            
        return redirect(reverse_lazy('login'))
    context ={'form': form}
    return render(request, 'login/login.html', context)

