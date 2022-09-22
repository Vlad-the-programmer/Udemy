from django.urls import path


from . import views

app_name = "orders"

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), 
                                                    name='orders'),
    path('order-create', views.OrderCreateView.as_view(), 
                                                    name='order-create'),
    path('order-update/<slug:slug>', views.OrderUpdateView.as_view(), 
                                                    name='order-update'),
    path('order-detail/<slug:slug>', views.OrderDetailView.as_view(), 
                                                    name='order-detail'),
    path('order-delete/<slug:slug>', views.OrderDeleteView.as_view(), 
                                                    name='order-delete'),
    
   
    
]

