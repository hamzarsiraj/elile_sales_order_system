from django.db import models
from django.utils import timezone

class ProductCategory(models.Model):
    ProductCategoryID = models.AutoField(primary_key=True)
    ParentProductCategory = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        db_column="ParentProductCategoryID"
    )
    Name = models.CharField(max_length=50)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField()

class ProductDescription(models.Model):
    ProductDescriptionID = models.IntegerField(primary_key=True)
    Description = models.CharField(max_length=400)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField()

class ProductModel(models.Model):
    ProductModelID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    CatalogDescription = models.TextField(null=True, blank=True)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField()
    ProductDescriptions = models.ManyToManyField(
        ProductDescription,
        db_table='SalesLT].[ProductModelProductDescription'
    )

class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    ProductNumber = models.CharField(max_length=25)
    Color = models.CharField(max_length=15, null=True, blank=True)
    StandardCost = models.DecimalField(max_digits=19, decimal_places=4)
    ListPrice = models.DecimalField(max_digits=19, decimal_places=4)
    Size = models.CharField(max_length=5, null=True, blank=True)
    Weight = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    ProductCategory = models.ForeignKey(
        ProductCategory,
        null=True,
        # if category is deleted, set it to null on product.
        on_delete=models.SET_NULL,
        related_name='ProductsByCategory',
        db_column='ProductCategoryID'
    )
    ProductModel = models.ForeignKey(
        ProductModel,
        null=True,
        # if model is deleted, set it to null on product.
        on_delete=models.SET_NULL,
        related_name='ProductsByModel',
        db_column='ProductModelID'
    )
    SellStartDate = models.DateTimeField()
    SellEndDate = models.DateTimeField(null=True, blank=True)
    DiscontinuedDate = models.DateTimeField(null=True, blank=True)
    ThumbnailPhoto = models.BinaryField(null=True, blank=True)
    ThumbnailPhotoFileName = models.CharField(max_length=50, null=True, blank=True)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField(default=timezone.now)
    class Meta:
        managed = False
        db_table = 'SalesLT].[Product'

class Address(models.Model):
    AddressID = models.AutoField(primary_key=True)
    AddressLine1 = models.CharField(max_length=60)
    AddressLine2 = models.CharField(max_length=60, null=True, blank=True)
    City = models.CharField(max_length=30)
    StateProvince = models.CharField(max_length=50)
    CountryRegion = models.CharField(max_length=50)
    PostalCode = models.CharField(max_length=15)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'SalesLT].[Address'

class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True)
    NameStyle = models.BooleanField()
    Title = models.CharField(max_length=8, null=True, blank=True)
    FirstName = models.CharField(max_length=50)
    MiddleName = models.CharField(max_length=50, null=True, blank=True)
    LastName = models.CharField(max_length=50)
    Suffix = models.CharField(max_length=10, null=True, blank=True)
    CompanyName = models.CharField(max_length=128, null=True, blank=True)
    SalesPerson = models.CharField(max_length=256, null=True, blank=True)
    EmailAddress = models.EmailField(max_length=50, null=True, blank=True)
    Phone = models.CharField(max_length=25, null=True, blank=True)
    PasswordHash = models.CharField(max_length=128)
    PasswordSalt = models.CharField(max_length=10)
    Addresses = models.ManyToManyField(
        Address,
        db_table='SalesLT].[CustomerAddress'
    )
    rowguid = models.UUIDField()
    class Meta:
        managed = False
        db_table = 'SalesLT].[Customer'

class SalesOrderHeader(models.Model):
    SalesOrderID = models.AutoField(primary_key=True)
    RevisionNumber = models.SmallIntegerField()
    OrderDate = models.DateTimeField()
    DueDate = models.DateTimeField()
    ShipDate = models.DateTimeField(null=True, blank=True)
    Status = models.SmallIntegerField()
    OnlineOrderFlag = models.BooleanField()
    SalesOrderNumber = models.CharField(max_length=25)
    PurchaseOrderNumber = models.CharField(max_length=25, null=True, blank=True)
    AccountNumber = models.CharField(max_length=15, null=True, blank=True)
    Customer = models.ForeignKey(
        Customer,
        # if customer is deleted, set CustomerID to -1 (special value to imdicate deleted customers, 
        # ideally we should enable soft delete for all entities and use an IsDeleted flag.)
        on_delete=models.SET(-1),
        related_name='Orders',
        db_column='CustomerID'
    )
    ShipToAddress = models.ForeignKey(
        Address,
        # we could either delete the order if it's address is deleted, or use models.PROTECT to prevent
        # deletion of an address that is associated with an order - since an order is useless without an address
        on_delete=models.CASCADE,
        related_name='ShipToAddressOrders',
        db_column='ShipToAddressID'
    )
    BillToAddress = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='BillToAddressOrders',
        db_column='BillToAddressID'
    )
    ShipMethod = models.CharField(max_length=50)
    CreditCardApprovalCode = models.CharField(max_length=15, null=True, blank=True)
    SubTotal = models.DecimalField(max_digits=19, decimal_places=4)
    TaxAmt = models.DecimalField(max_digits=19, decimal_places=4)
    Freight = models.DecimalField(max_digits=19, decimal_places=4)
    TotalDue = models.DecimalField(max_digits=19, decimal_places=4)
    Comment = models.TextField(null=True, blank=True)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'SalesLT].[SalesOrderHeader'

class SalesOrderDetail(models.Model):
    SalesOrderDetailID = models.AutoField(primary_key=True)
    SalesOrder = models.ForeignKey(
        SalesOrderHeader,
        # delete order detail if the order is deleted
        on_delete=models.CASCADE,
        related_name='OrderDetails',
        db_column='SalesOrderID'
    )
    OrderQty = models.SmallIntegerField()
    Product = models.ForeignKey(
        Product,
        # delete order detail if the product is deleted
        on_delete=models.CASCADE,
        related_name='Products',
        db_column='ProductID'
    )
    UnitPrice = models.DecimalField(max_digits=19, decimal_places=4)
    UnitPriceDiscount = models.DecimalField(max_digits=19, decimal_places=4)
    LineTotal = models.DecimalField(max_digits=19, decimal_places=4)
    rowguid = models.UUIDField()
    ModifiedDate = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'SalesLT].[SalesOrderDetail'