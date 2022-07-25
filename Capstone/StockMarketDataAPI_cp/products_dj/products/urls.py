from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductRetrieveListApi.as_view(), name='product'),
    path('store/', views.store, name='store')

]