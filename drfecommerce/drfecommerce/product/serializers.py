from rest_framework import serializers

from .models import Category, Product, Brand, ProductLine


class CategorySerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(source='name')
    # here we change name to category name category.name == 'category_name'

    class Meta:
        model = Category
        fields = ['category_name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('id',)


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ('id', 'product', 'is_active')


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name')  # product.brand.name == 'brand_name'
    # category = CategorySerializer()  # Without serializers only ID of category and brand will be returned
    category_name = serializers.CharField(source='category.name')
    product_line = ProductLineSerializer(many=True)  # If our serializer returns more than one instance of data
    # we have to set many=True

    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'brand_name', 'category_name', 'product_line')
