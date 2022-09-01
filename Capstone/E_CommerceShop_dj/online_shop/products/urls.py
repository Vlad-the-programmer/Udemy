from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('products/', views.ProductRetrieveListApi.as_view(), name='products'),
    path('add-product/', views.CreateProductView.as_view(), name='add-product'),
    path('update-product/<int:pk>', views.UpdateProductView.as_view(), name='update-product')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    