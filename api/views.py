from django.shortcuts import render
from inventory.models import Product, ProductInventory
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# ესეიგი ეს ყველაფერი გვჭირდება ეიპიაისთვის

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from .serializers import *

# Create your views here.

class AllProductView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # მოკლედ ეს ორი გვჭირდება აუცილებლად სერიალაიზერ კლასი და მონაცემები
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer

    # ესენი უკვე რაღაც ფუნქციაებია რომელიც იგივე რაღაცეებს აკეთებს
    @method_decorator(cache_page(60 * 15))
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer

    lookup_field = 'sku'