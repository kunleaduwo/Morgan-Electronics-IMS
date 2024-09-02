from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Inventory
from .forms import AddInventoryForm, UpdateInventoryForm

from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json



@login_required
def products_list(request):
    inventories = Inventory.objects.all()
    context = {

        "title":"Products List",
        "inventories": inventories
    }
    return render(request, "inventory/products_list.html", context=context)



@login_required
def product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }

    return render(request, "./inventory/product_view.html", context=context)

@login_required
def add_product(request): 
    if request.method == "POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_product = add_form.save(commit=False)
            new_product.sales = float(add_form.data['product_cost']) * float(add_form.data['sold_quantity'])
            new_product.save()
            messages.success(request, "Product has been added successfully")
            return redirect("/inventory/")
        
    else:
        add_form = AddInventoryForm()
        
    return render(request, "./inventory/add_product.html", {"form": add_form})


@login_required
def delete_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, "Product has been deleted.")
    return redirect("/inventory/")

@login_required
def update_product(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        UpdateForm = UpdateInventoryForm(data=request.POST)
        if UpdateForm.is_valid():
            inventory.product_name = UpdateForm.data['product_name']
            inventory.stock_quantity = UpdateForm.data['stock_quantity']
            inventory.sold_quantity = UpdateForm.data['sold_quantity']
            inventory.product_cost= UpdateForm.data['product_cost']
            inventory.sales = float(inventory.product_cost) * float(inventory.sold_quantity)
            inventory.save()
            messages.success(request, "Product has been updated.")
            return redirect(f"/inventory/product_details/{pk}")
    
    else:
        UpdateForm = UpdateInventoryForm(instance=inventory)
    context = {"form": UpdateForm}
    return render(request, "./inventory/product_update.html", context=context)



@login_required
def dashboard(request):
    inventories = Inventory.objects.all()
    
    df = read_frame(inventories)
    
    sales_graph = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
    sales_graph = px.line(sales_graph, x = sales_graph.last_sales_date, y = sales_graph.sales, title="SALES TREND")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)
    
    best_selling_product_df = df.groupby(by="product_name") .sum().sort_values(by="sold_quantity")
    best_selling_product = px.bar(best_selling_product_df,
                                  x = best_selling_product_df.index,
                                  y = best_selling_product_df.sold_quantity,
                                  title = "BEST SELLING PRODUCT"
                                  )
    
    best_selling_product = json.dumps(best_selling_product, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    
    
    most_product_in_stock_df = df.groupby(by="product_name").sum().sort_values(by="stock_quantity")
    most_product_in_stock = px.pie(most_product_in_stock_df,
                                   names=most_product_in_stock_df.index,
                                   values=most_product_in_stock_df.stock_quantity,
                                   title="HIGHEST PRODUCT IN STOCK"
                                   )
    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)
    
    context = {
        "sales_graph": sales_graph,
        "best_selling_product": best_selling_product,
        "most_product_in_stock" : most_product_in_stock
    }
    
    return render(request, "inventory/dashboard.html", context=context)