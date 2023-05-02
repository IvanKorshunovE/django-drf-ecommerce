from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format


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

    # queryset = Product.isactive.all() Part 65
    queryset = Product.objects.all().isactive()  # models.py - line 6
    lookup_field = 'slug'  # The lookup_field attribute defaults to 'pk', which is the primary key of the model.

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related('category', 'brand'),
            many=True
        )
        data = Response(serializer.data)
        q = list(connection.queries)
        print(len(q))
        for qs in q:
            sqlformatted = format(str(qs['sql']), reindent=True)
            print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))
        # x = self.queryset.filter(slug=slug)
        # sqlformatted = format(str(x.query), reindent=True)
        # print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))
        return data

    @extend_schema(responses=ProductSerializer)  # this telling drf-spectacular what serializers we are using
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)  # We prepared that data for sending to Frontend
        return Response(serializer.data)

    @action(
        methods=['get'],
        detail=False,  # detail = if current action configured for a list or a detail view
        url_path=r'category/(?P<slug>[\w-]+)',
        # url_path=r'category/' is a prefix after the product - api/product/category/++++/all, P - 0 or 1 occurence
        # \w = characters lowercase, numbers 0-9 and _
        # url_name='all'
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to return product by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__slug=slug), many=True)
        return Response(serializer.data)
