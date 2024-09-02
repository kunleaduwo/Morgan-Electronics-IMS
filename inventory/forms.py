from django.forms import ModelForm 
from . models import Inventory

class AddInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['product_name', 'product_cost', 'stock_quantity', 'sold_quantity']


class UpdateInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['product_name', 'product_cost', 'stock_quantity', 'sold_quantity']
