from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=101, unique=True)  # Parent category
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insetrion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=101, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=101)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)  # Downloadable or not
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # What happens if we delete brand
    category = TreeForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)  # If delete category =
    # this field is set to NULL

    def __str__(self):
        return self.name

