from django.urls import path

from products import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/add_product', views.add_product, name='add_product'),
    path('product/product_list', views.product_list, name='product_list'),
    path('product/product_update/<int:id>/', views.product_update, name='product_update'),
    path('product/product_delete/<int:id>/', views.product_delete, name='product_delete')
]
