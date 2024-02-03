from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newhome', views.newhome, name='newhome'),
    path('signup/', views.signup, name='signup'),
    path('user_login', views.user_login, name='user_login'),
    path('account/', views.account, name='account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('womens', views.womens, name='womens'),
    path('accessories', views.accessories, name='accessories'),
    path('brides', views.brides, name='brides'),
    path('lg_out', views.lg_out, name='lg_out'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('order_confirmation', views.order_confirmation, name='order_confirmation'),
    path('add_product', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product_view', views.product_view, name='product_view'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
]
