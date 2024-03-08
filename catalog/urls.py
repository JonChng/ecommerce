from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_catalog),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name='login')
]
