from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("collections/<slug:slug>", views.collections, name="collections"),
    path("product_detail/<slug:slug>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),

    # for filter products using ajax
    path('filter_products/', views.filter_products, name='filter_products'),
    path('filter_products_for_collections/', views.filter_products_for_collections, name='filter_products_for_collections'),
    
    path('filter_products_for_productDtl/', views.filter_products_for_productDtl, name='filter_products_for_productDtl'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('get_cart_data/', views.get_cart_data, name='get_cart_data'),
    path('updateCart/', views.updateCart, name='updateCart'),
    path('processOrder/', views.processOrder, name='processOrder'),
]