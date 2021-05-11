from django.urls import path

from orders import views

urlpatterns = [
    # order urls
    path('order/', views.order_list, name='order_list'),             # order list
    path('order/add_order', views.add_order, name='add_order'),      # input customer
    path('order/order_product/<int:order_id>', views.order_product, name='order_product'),       # show item that'll add
    path('order/order_details/<int:order_id>', views.order_details, name='order_details'),       # show added item
    path('order/confirm_order/<int:order_id>', views.confirm_order, name='confirm_order'),       # confirm order
    path('order/order_invoice/<int:order_id>', views.order_invoice, name='order_invoice'),       # Generate invoice
    path('order/download_invoice/<int:order_id>', views.download_invoice, name='download_invoice'),  # Download pdf

    # item urls
    path('order/add_item', views.add_item, name='add_item'),             # create item
    path('order/update_item', views.update_item, name='update_item'),    # update item
    path('order/delete_item/<int:item_id>', views.delete_item, name='delete_item'),  # delete item
]
