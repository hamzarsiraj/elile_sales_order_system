from django.db import connection
from django.http import Http404
from elile_sales_order_system.settings import DEFAULT_PAGE_SIZE

def get_order_details_sql(context, request, order_id):
    """
        Retrieves details of an order by its ID.

        Args:
            context: The current context.
            request: The incoming HTTP request.
            order_id: The ID of the order to retrieve the details for.

        Returns:
            A list of order details.
    """
        
    with connection.cursor() as cursor:
        context.page_number = request.GET.get("page_number", 1)
        context.page_size = request.GET.get("page_size", DEFAULT_PAGE_SIZE)

        cursor.execute("SELECT soh.OrderDate, soh.DueDate, soh.TotalDue, soh.TaxAmt, soh.Freight, soh.Status, " +
	            "CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName, c.EmailAddress, c.Phone, " +
	            "CONCAT(a1.AddressLine1, ', ', a1.AddressLine2, ', ', a2.City) AS ShipToAddress, " + 
	            "CONCAT(a2.AddressLine1, ', ', a2.AddressLine2, ', ', a2.City) AS BillToAddress, " +
	            "p.ProductID, p.Name as ProductName, sod.OrderQty, sod.UnitPrice, sod.LineTotal " +
	            "FROM SalesLT.SalesOrderDetail sod " +
	            "JOIN SalesLT.SalesOrderHeader soh ON soh.SalesOrderID = sod.SalesOrderID " +
	            "JOIN SalesLT.Customer c ON c.CustomerID = soh.CustomerID " +
	            "JOIN SalesLT.Address a1 on a1.AddressID = soh.ShipToAddressID " +
	            "JOIN SalesLT.Address a2 on a2.AddressID = soh.BillToAddressID " +
	            "JOIN SalesLT.Product p on p.ProductID = sod.ProductID " +
                "WHERE soh.SalesOrderID = %s " +
                "ORDER BY p.ProductID " + 
                "OFFSET(%s - 1) * %s ROWS " + 
                "FETCH NEXT %s ROWS ONLY", 
                [int(order_id), int(context.page_number), int(context.page_size), int(context.page_size)])
        rows = cursor.fetchall()

        if (len(rows) == 0):
            raise Http404("Order with id: " + order_id + " does not exist.")

        data = []
        for row in rows:
            data.append({
                'OrderDate': row[0],
                'DueDate': row[1],
                'TotalDue': row[2],
                'TaxAmt': row[3],
                'Freight': row[4],
                'Status': row[5],
                'CustomerName': row[6],
                'EmailAddress': row[7],
                'Phone': row[8],
                'ShipToAddress': row[9],
                'BillToAddress': row[10],
                'ProductID': row[11],
                'ProductName': row[12],
                'OrderQty': row[13],
                'UnitPrice': row[14],
                'LineTotal': row[15]
            })

        return data

def get_customer_orders_sql(context, request, customer_id):
    """
        Retrieves orders placed by a customer by their ID.

        Args:
            context: The current context.
            request: The incoming HTTP request.
            customer_id: The ID of the customer to retrieve the orders of.

        Returns:
            A list of customer orders.
    """
     
    with connection.cursor() as cursor:
        context.page_number = request.GET.get("page_number", 1)
        context.page_size = request.GET.get("page_size", DEFAULT_PAGE_SIZE)

        cursor.execute("SELECT soh.SalesOrderID, soh.OrderDate, soh.TotalDue, p.Name, sod.OrderQty " +
	            "FROM SalesLT.SalesOrderHeader soh " + 
	            "JOIN SalesLT.Customer c ON soh.CustomerID = c.CustomerID " +
	            "JOIN SalesLT.SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID " +
	            "JOIN SalesLT.Product p ON p.ProductID = sod.ProductID " +
	            "WHERE soh.CustomerID = %s " +
                "ORDER BY p.ProductID " + 
                "OFFSET(%s - 1) * %s ROWS " +
                "FETCH NEXT %s ROWS ONLY", 
                [int(customer_id), int(context.page_number), int(context.page_size), int(context.page_size)])
        rows = cursor.fetchall()

        if (len(rows) == 0):
            raise Http404("No orders were found for customer with id: " + customer_id)

        data = []
        for row in rows:
            data.append({
                'SalesOrderID': row[0],
                'OrderDate': row[1],
                'TotalDue': row[2],
                'ProductName': row[3],
                'OrderQty': row[4]
            })

        return data
    
def get_discounted_orders_sql(context, request):
    """
        Retrieves all discounted orders.

        Args:
            context: The current context.
            request: The incoming HTTP request.        

        Returns:
            A list of discounted orders.
    """
        
    with connection.cursor() as cursor:
        context.page_number = request.GET.get("page_number", 1)
        context.page_size = request.GET.get("page_size", DEFAULT_PAGE_SIZE)

        cursor.execute("SELECT soh.SalesOrderID, p.ProductID, p.Name as ProductName, sod.OrderQty, sod.UnitPriceDiscount,sod.LineTotal " +
                            "FROM SalesLT.SalesOrderDetail sod " +
	                        "JOIN SalesLT.SalesOrderHeader soh on soh.SalesOrderID = sod.SalesOrderID " +
	                        "JOIN SalesLT.Product p ON p.ProductID = sod.ProductID " +
	                        "WHERE sod.UnitPriceDiscount > 0 " + 
                            "ORDER BY p.ProductID " + 
                            "OFFSET(%s - 1) * %s ROWS " +
                            "FETCH NEXT %s ROWS ONLY", 
                            [int(context.page_number), int(context.page_size), int(context.page_size)])
        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                'SalesOrderID': row[0],
                'ProductID': row[1],
                'ProductName': row[2],
                'OrderQty': row[3],
                'UnitPriceDiscount': row[4],
                'LineTotal': row[5]
            })
        
        return data