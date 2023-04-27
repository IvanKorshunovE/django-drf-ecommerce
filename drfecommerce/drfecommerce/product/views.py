from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)  # this telling drf-spectacular what serializers we are using
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)  # We prepared that data for sending to Frontend
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing categories
    """

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)  # this telling drf-spectacular what serializers we are using
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)  # We prepared that data for sending to Frontend
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple viewset for viewing categories
    """

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)  # this telling drf-spectacular what serializers we are using
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)  # We prepared that data for sending to Frontend
        return Response(serializer.data)