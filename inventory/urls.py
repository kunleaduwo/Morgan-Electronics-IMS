from django.urls import path
from .views import (products_list,
                    product_view,
                    add_product, 
                    delete_product,
                    update_product,
                    dashboard
                     )

urlpatterns = [
    path('', products_list, name='products_list'),
    path('product_details/<int:pk>', product_view, name='product_details'),
    path("add_product/", add_product, name="add_product"),
    path("delete/<int:pk>", delete_product, name="delete_product"),
    path("update/<int:pk>", update_product, name="update_product"),
    path("dashboard/", dashboard, name="dashboard")
    
    
]