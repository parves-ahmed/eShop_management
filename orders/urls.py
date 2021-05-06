from django.urls import path

from orders import views

urlpatterns = [
    path('order/add_order', views.add_order, name='add_order'),
    path('order/order_product/<int:order_id>', views.order_product, name='order_product'),
    path('order/order_details/<int:order_id>', views.order_details, name='order_details'),
    path('order/confirm_order', views.confirm_order, name='confirm_order'),
    path('order/add_item', views.add_item, name='add_item'),
    path('order/update_item', views.update_item, name='update_item'),
    path('order/delete_item/<int:item_id>', views.delete_item, name='delete_item'),
]
