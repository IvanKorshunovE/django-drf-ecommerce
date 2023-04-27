from rest_framework import serializers

from .models import Category, Product, Brand


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    brand = BrandSerializer()
    category = CategorySerializer()  # Without serializers only ID of category and brand will be returned

    class Meta:
        model = Product
        fields = "__all__"

