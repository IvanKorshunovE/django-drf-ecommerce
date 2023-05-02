import pytest
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        x = category_factory(name='t_cat')
        assert x.__str__() == 't_cat'

class TestBrandModel:
    def test_str_method(self, brand_factory):
        x = brand_factory(name='test_brand')
        print('Hello')
        assert x.__str__() == 'test_brand'


class TestProductModel:
    def test_str_method(self, product_factory):
        x = product_factory(name='test_product')
        assert x.__str__() == 'test_product'



class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku='12345')
        assert obj.__str__() == '12345'

    def test_dupclicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

