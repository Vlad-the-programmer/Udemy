from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('register/', views.signup, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(
                            template_name='login/login.html',
                            success_url='products/'), 
                            name='login'
                            ),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    