from django.db import models

class Inventory(models.Model):
    product_name = models.CharField(max_length=300, null=False, blank=False)
    product_cost = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_quantity = models.IntegerField(null=False, blank=False)
    sold_quantity = models.IntegerField(null=False, blank=False)
    sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)


    def __str__(self) -> str:
        return self.product_name