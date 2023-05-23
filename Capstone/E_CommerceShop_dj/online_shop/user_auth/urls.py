from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user-auth'

urlpatterns = [

    path('register/', views.SignUpView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(
                                            template_name='auth/login/login.html',
                                            success_url='products/'),
                                            name='login'
                                            ),
    path('accounts/logout/', auth_views.LogoutView.as_view(),
                                            name='logout'),
    path('profile-detail/<uuid:pk>/', views.ProfileDetailView.as_view(),
                                            name='profile-detail'),
    path('profile-update/<uuid:pk>/', views.UpdateProfileView.as_view(),
                                            name='profile-update'),
    path('profile-delete/<uuid:pk>/', views.DeleteProfileView.as_view(),
                                            name='profile-delete'),
    
    
    
] 

