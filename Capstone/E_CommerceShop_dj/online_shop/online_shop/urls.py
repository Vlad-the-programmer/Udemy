
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('user_auth.urls')),
    path('order/', include('orders.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls'))
]
