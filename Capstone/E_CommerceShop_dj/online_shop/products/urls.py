from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('products/', views.ProductRetrieveListApi.as_view(), name='products'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(
                            template_name='products/login/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')

]