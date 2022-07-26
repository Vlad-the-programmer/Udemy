from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductRetrieveListApi.as_view(), name='product'),
    path('register/', views.SignUpView.as_view(), name='register')

]