from django.urls import path
from . import views

urlpatterns = [
    path("products/<str:sku>", views.ProductDetailAPIView.as_view(), name="ProductView"),
    path("products/", views.AllProductView.as_view(), name="AllProductView"),
]