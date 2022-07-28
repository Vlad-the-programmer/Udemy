from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductRetrieveListApi.as_view(), name='products'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout')



]