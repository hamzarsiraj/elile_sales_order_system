from django.urls import path, re_path
from elile_sales_order_api import views

urlpatterns = [
    # URLs for ORM based APIs
    re_path(r'^customer-orders/([0-9]+)$', views.CustomerOrdersOrmView.as_view()),
    re_path(r'^order-details/([0-9]+)$', views.OrderDetailsOrmView.as_view()),
    path('discounted-orders', views.DiscountedOrdersOrmView.as_view()),
    # URLs for Raw SQL based APIs
    re_path(r'^customer-orders-raw/([0-9]+)$', views.CustomerOrdersRawSqlView.as_view()),
    re_path(r'^order-details-raw/([0-9]+)$', views.OrderDetailsRawSqlView.as_view()),
    path('discounted-orders-raw', views.DiscountedOrdersRawSqlView.as_view())
]