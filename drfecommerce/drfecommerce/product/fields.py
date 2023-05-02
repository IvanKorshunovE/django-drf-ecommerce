from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = 'Ordering field on a unique field'

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        # The unique_for_field argument will be passed as a keyword argument to the __init__ method of
        # the OrderField class, and *args and **kwargs will capture any other arguments that are passed
        # (in this case, blank=True). These arguments will then be passed to the __init__ method of the parent class
        # (PositiveIntegerField), which will handle them according to its own implementation.
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs)  # list has no attribute level
        ]

    def _check_for_field_attribute(self, **kwargs):
        """
        If we do not include 'unique_for_field=----- then it will throw an error,
        example: order = OrderField(blank=True) -- should be: order = OrderField(unique_for_field='product', blank=True)
        """
        if self.unique_for_field is None:
            return [
                checks.Error(
                    "Order field must define a 'unique_for_field' attribute"
                )
            ]
        elif self.unique_for_field not in [f.name for f in self.model._meta.get_fields()]:
            # that is going to grab the list of all fields in table
            return [
                checks.Error(
                    "Order field must be in the table (OrderField entered does not match an existing model fiedl)"
                )
            ]
        return []

    def pre_save(self, model_instance, add):
        print(model_instance)

        if getattr(model_instance, self.attname) is None:  # Since the class we created is OrderField,
            # self.attname = order!!! (look at the name of this class!)

            qs = self.model.objects.all()  # returns all the product line data
            try:
                query = {self.unique_for_field: getattr(model_instance, self.unique_for_field)}  # {'product': <Product: p1>}
                #  getattr(model_instance, self.unique_for_field) product related to a saved product line instance
                #  is returned
                print(query)
                qs = qs.filter(**query)  # Filter out particular product (product_line)
                last_item = qs.latest(self.attname)  # the highest order number
                value = last_item.order + 1
                print(qs)
            except ObjectDoesNotExist:
                value = 1
            return value  # Returns a product_line.order
        else:
            return super().pre_save(model_instance, add)
