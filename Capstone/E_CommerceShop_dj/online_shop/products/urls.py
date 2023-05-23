from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.ProductRetrieveListApi.as_view(), name='products'),
    path('add-product/', views.CreateProductView.as_view(), name='add-product'),
    path('update-product/<slug:slug>', views.UpdateProductView.as_view(), name='update-product'),
    path('delete-product/<slug:slug>', views.DeleteProductView.as_view(), name='delete-product'),
    path('detail-product/<slug:slug>', views.DetailProductView.as_view(), name='product-detail')
    
    
]

