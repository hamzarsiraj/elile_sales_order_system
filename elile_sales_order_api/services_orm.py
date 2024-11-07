from django.http import Http404
from elile_sales_order_api.models import SalesOrderHeader
from elile_sales_order_system.settings import DEFAULT_PAGE_SIZE

def get_order_details(order_id):
    """
        Retrieves details of an order by its ID.

        Args:
            order_id: The ID of the order to retrieve the details for.

        Returns:
            A list of order details.
    """
    
    orders = SalesOrderHeader.objects.select_related(
        'Customer',
        'ShipToAddress',
        'BillToAddress'
    ).filter(
        SalesOrderID = order_id
    ).prefetch_related(
        'OrderDetails',
        'OrderDetails__Product'
    )

    if (len(orders) == 0):
        raise Http404('Order with ID: ' + order_id + ' not found.')

    order_data = []
    for order in orders:
        order_details = []
        for detail in order.OrderDetails.all():
            order_details.append({
                'Product': detail.Product,
                'UnitPrice': detail.UnitPrice,
                'OrderQty': detail.OrderQty,
                'LineTotal': detail.LineTotal
            })
        order_data.append({
            'Customer': order.Customer,
            'OrderDate': order.OrderDate,
            'DueDate': order.DueDate,
            'TotalDue': order.TotalDue,
            'SalesOrderDetail': order_details,
            'ShipToAddress': order.ShipToAddress,
            'BillToAddress': order.BillToAddress
        })

    return order_data

def get_customer_orders(customer_id):
    """
        Retrieves orders placed by a customer by their ID.

        Args:
            customer_id: The ID of the customer to retrieve the orders of.

        Returns:
            A list of customer orders.
    """

    orders = SalesOrderHeader.objects.select_related(
        'Customer',
    ).filter(
        Customer = customer_id
    ).prefetch_related(
        'OrderDetails',
        'OrderDetails__Product'
    )

    if (len(orders) == 0):
        raise Http404("No orders were found for customer with id: " + customer_id)

    order_data = []
    for order in orders:
        order_details = []
        for detail in order.OrderDetails.all():
            order_details.append({
                'Product': detail.Product,
                'UnitPrice': detail.UnitPrice,
                'OrderQty': detail.OrderQty,
                'LineTotal': detail.LineTotal
            })
        order_data.append({
            'SalesOrderID': order.SalesOrderID,
            'OrderDate': order.OrderDate,
            'TotalDue': order.TotalDue,
            'SalesOrderDetail': order_details
        })

    return order_data

def get_discounted_orders():
    """
        Retrieves all discounted orders.

        Returns:
            A list of discounted orders.
    """

    orders_with_discount = SalesOrderHeader.objects.select_related(
        'Customer'
    ).prefetch_related(
        'OrderDetails',
        'OrderDetails__Product'
    ).filter(
        OrderDetails__UnitPriceDiscount__gt = 0
    )

    order_data = []
    for order in orders_with_discount:
        order_details = []
        for detail in order.OrderDetails.all():
            order_details.append({
                'Product': detail.Product,
                'OrderQty': detail.OrderQty,
                'UnitPrice': detail.UnitPrice,
                'Discount': detail.UnitPriceDiscount,
                'LineTotal': detail.LineTotal
            })
        order_data.append({
            'SalesOrderDetail': order_details,
            'OrderDate': order.OrderDate,
            'TotalDue': order.TotalDue
        })

    return order_data