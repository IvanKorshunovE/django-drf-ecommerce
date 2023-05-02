from django.db import models
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField



# Create your models here.
class ActiveQueryset(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)



# class ActiveManager(models.Manager):  # Filter not active products
#     # def get_queryset(self):
#     #     return super().get_queryset().filter(is_active=True)  # call the get_queryset method and add filter. part 65
#     def isactive(self):
#         return self.get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=101, unique=True)  # Parent category
    slug = models.SlugField(max_length=255)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insetrion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=101, unique=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=101)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)  # Downloadable or not
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # What happens if we delete brand
    category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)  # If delete category =
    # this field is set to NULL
    is_active = models.BooleanField(default=False)

    # Custom queryset manager
    objects = ActiveQueryset.as_manager()
    # isactive = ActiveManager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField() # stock_quantity
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_line')
    is_active = models.BooleanField(default=False)  # Not available to search, for example seasonal products
    order = OrderField(unique_for_field='product', blank=True)

    objects = ActiveQueryset.as_manager()

    def clean(self, exclude=None):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:  # self.id = is the instance that we are saving
                # if elf.id == obj.id and self.order == obj.order - IT COULD BE THE SAME product_line instance that we
                # are saving
                raise ValidationError('Duplicate value')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)

