from django.http.response import JsonResponse
from django.http import Http404
from elile_sales_order_api.serializers import OrderSerializer
from elile_sales_order_api.services_orm import get_order_details, get_customer_orders, get_discounted_orders
from elile_sales_order_api.services_sql import get_order_details_sql, get_customer_orders_sql, get_discounted_orders_sql
from elile_sales_order_system.settings import DEFAULT_PAGE_SIZE
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

class OrderDetailsOrmView(APIView, PageNumberPagination):
    '''
    List all details an order.

    Note: Uses Django ORM. See OrderDetailsRawSqlView for a raw SQL version.
    '''

    def get(self, request, order_id):
        """
        Retrieves details of an order by its ID.

        Args:
            request: The incoming HTTP request.
            order_id: The ID of the order to retrieve the details for.
            page_size: Number of items to be returned (Default 5).
            page_number: Page number (Default 1).

        Returns:
            An HTTP response containing the serialized order data.
        """

        order_data = get_order_details(order_id=order_id)

        self.page_number = request.GET.get("page_number", 1)
        self.page_size = request.GET.get("page_size", DEFAULT_PAGE_SIZE)
        results = self.paginate_queryset(order_data, request, view=self)
        
        order_serializer = OrderSerializer(results, many=True)
        return self.get_paginated_response(order_serializer.data)

class CustomerOrdersOrmView(APIView, PageNumberPagination):
    '''
    List all orders placed by a customer.

    Note: Uses Django ORM. See CustomerOrdersRawSqlView for a raw SQL version.
    '''

    def get(self, request, customer_id):
        """
        Retrieves orders placed by a customer by their ID.

        Args:
            request: The incoming HTTP request.
            customer_id: The ID of the customer to retrieve the orders of.
            page_size: Number of items to be returned (Default 5).
            page_number: Page number (Default 1).

        Returns:
            An HTTP response containing the serialized order data.
        """
         
        order_data = get_customer_orders(customer_id=customer_id)
                
        self.page_number = request.GET.get("page_number", 1)
        self.page_size = request.GET.get("page_size", DEFAULT_PAGE_SIZE)
        results = self.paginate_queryset(order_data, request, view=self)

        order_serializer = OrderSerializer(results, many=True)
        return self.get_paginated_response(order_serializer.data)
    
class DiscountedOrdersOrmView(APIView, PageNumberPagination):
    '''
    List all discounted orders.

    Note: Uses Django ORM. See DiscountedOrdersRawSqlView for a raw SQL version.
    '''

    def get(self, request):
        """
        Retrieves all discounted orders.

        Args:
            request: The incoming HTTP request.
            page_size: Number of items to be returned (Default 5).
            page_number: Page number (Default 1).

        Returns:
            An HTTP response containing the serialized order data.
        """

        order_data = get_discounted_orders()

        self.page_number = request.GET.get("page_number", 1)
        self.page_size = request.GET.get("page_size", DEFAULT_PAGE_SIZE)
        results = self.paginate_queryset(order_data, request, view=self)

        order_serializer = OrderSerializer(results, many=True)
        return self.get_paginated_response(order_serializer.data)

class OrderDetailsRawSqlView(APIView):
    '''
    List all details an order.

    Note: uses raw SQL. See OrderDetailsOrmView for an ORM version.
    '''

    def get(self, request, order_id):
        """
        Retrieves details of an order by its ID.

        Args:
            request: The incoming HTTP request.
            order_id: The ID of the order to retrieve the details for.
            page_size: Number of items to be returned (Default 5).
            page_number: Page number (Default 1).

        Returns:
            An HTTP response containing the serialized order data.
        """

        order_data = get_order_details_sql(context=self, request=request, order_id=order_id)
        return JsonResponse(order_data, safe = False)

class CustomerOrdersRawSqlView(APIView):
    '''
    List all orders placed by a customer.

    Note: uses raw SQL. See CustomerOrdersOrmView for an ORM version.
    '''

    def get(self, request, customer_id):
        """
        Retrieves orders placed by a customer by their ID.

        Args:
            request: The incoming HTTP request.
            customer_id: The ID of the customer to retrieve the orders of.
            page_size: Number of items to be returned (Default 5).
            page_number: Page number (Default 1).

        Returns:
            An HTTP response containing the serialized order data.
        """

        order_data = get_customer_orders_sql(context=self, request=request, customer_id=customer_id)
        return JsonResponse(order_data, safe = False)
    
class DiscountedOrdersRawSqlView(APIView):
    '''
    List all discounted orders.

    Note: uses raw SQL. See DiscountedOrdersOrmView for an ORM version.
    '''

    def get(self, request):
        """
        Retrieves all discounted orders.

        Args:
            request: The incoming HTTP request.
            page_size: Number of items to be returned (Default 5).
            page_number: Page number (Default 1).

        Returns:
            An HTTP response containing the serialized order data.
        """

        order_data = get_discounted_orders_sql(context=self, request=request)
        return JsonResponse(order_data, safe = False)
