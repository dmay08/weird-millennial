from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'), #have to use 'pk' for DetailView
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('increase_qty/<int:line_item_id>', views.increase_qty, name='increase_qty'), # use <int:___> for URLS.py
    path('decrease_qty/<int:line_item_id>', views.decrease_qty, name='decrease_qty'),
]