from django.urls import path
from . import views

urlpatterns = [
    path('exchange/', views.CurrencyExchangeView.as_view(), name='exchange')
]