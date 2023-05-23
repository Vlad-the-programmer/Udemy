from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path('item-update/',             views.updateItem,   name='item-update'),
    path('checkout/',                views.checkout,     name='checkout'),
    path('process-order/',           views.processOrder, name='process-order'),
    path('cart/',                    views.CartView.as_view(), 
                                                         name='cart'),
    path('cookie-cart/',             views.CookieCartView.as_view(),
                                                         name='cookie-cart'),
    path('order-create',             views.OrderCreateView.as_view(), 
                                                         name='order-create'),
    path('order-detail/<slug:slug>', views.OrderDetailView.as_view(), 
                                                         name='order-detail'),
    path('order-delete/<slug:slug>', views.OrderDeleteView.as_view(), 
                                                         name='order-delete'),
   
    
]

