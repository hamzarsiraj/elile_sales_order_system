from rest_framework import serializers
from elile_sales_order_api.models import Address, Product, Customer, SalesOrderHeader, SalesOrderDetail

class ProductSerializer(serializers.ModelSerializer):
    '''
    Serializer for Product.

    Creates a minimal representation of a Product.
    '''
    
    class Meta:
        model = Product
        fields = ['ProductID', 'Name', 'ProductNumber']

class CustomerSerializer(serializers.ModelSerializer):
    '''
    Serializer for Customer.

    Creates a minimal representation of a Customer.
    '''

    class Meta:
        model = Customer
        fields = ['CustomerID', 'FirstName', 'LastName', 'EmailAddress', 'Phone']

class SalesOrderDetailSerializer(serializers.ModelSerializer):
    '''
    Serializer for SalesOrderDetail.

    Creates a minimal representation of a SaleOrderDetail.
    '''

    Product = ProductSerializer(read_only=True)

    class Meta:
        model = SalesOrderDetail
        fields = ['Product', 'OrderQty', 'UnitPrice', 'LineTotal']

class AddressSerializer(serializers.ModelSerializer):
    '''
    Serializer for Address.

    Creates a minimal representation of an Address.
    '''

    class Meta:
        model = Address
        fields = ['AddressLine1', 'AddressLine2', 'City', 'PostalCode']

class OrderSerializer(serializers.ModelSerializer):
    '''
    Serializer for SalesOrderHeader.

    Creates a minimal representation of an Order.
    '''

    Customer = CustomerSerializer(read_only=True)
    SalesOrderDetail = SalesOrderDetailSerializer(many=True, read_only=True)
    ShipToAddress = AddressSerializer(read_only=True)
    BillToAddress = AddressSerializer(read_only=True)
    class Meta:
        model = SalesOrderHeader
        fields = ['Customer', 'SalesOrderID', 'OrderDate', 'TotalDue', 
                  'SalesOrderDetail', 'ShipToAddress', 'BillToAddress']