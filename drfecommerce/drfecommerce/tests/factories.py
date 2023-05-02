import factory
import pytest

from drfecommerce.product.models import Category, Brand, Product, ProductLine


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # name = "test_category"
    name = factory.sequence(lambda n: 'Category_%d' % n)  # Category_1 Category_2 Category_3


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.sequence(lambda n: 'Brand_%d' % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "test_product"
    description = 'test_description'
    is_digital = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    is_active = True



class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = '12345'
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True



