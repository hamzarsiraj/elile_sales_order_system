Project structure:

Settings: elile_sales_order_system.settings.py

Models: elile_sales_order_api.models.py
Serializers: elile_sales_order_api.serializers.py

Services: 
1) elile_sales_order_api.services_orm.py - ORM version of data retrieval
2) elile_sales_order_api.services_sql.py - Raw SQL version of data retrieval

URLs: elile_sales_order_api.urls.py
Views: elile_sales_order_api.views.py

Tests: elile_sales_order_api/tests

---------------------------------------------------

There were 3 endpoints required to be created:
1. order-details/<order_id>
2. customer-orders/<customer_id>
3. discounted-orders

Notes: 
1. The implementation consists of both an ORM and a raw SQL version for all the endpoints. See the views.py file.
    - To access the raw SQL versions, just add the "-raw" suffix to the URL, for e.g. use "order-details-raw/<order_id>" for the first endpoint. See the URLs file.

2. All serializers generate a minimal representation of the entities required by the above 3 endpoints.

---------------------------------------------------


Generated responses:

1. /order-details/<order_id>

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "Customer": {
                "CustomerID": 30113,
                "FirstName": "Raja",
                "LastName": "Venugopal",
                "EmailAddress": "raja0@adventure-works.com",
                "Phone": "1 (11) 500 555-0195"
            },
            "OrderDate": "2008-06-01T00:00:00Z",
            "TotalDue": "42452.6519",
            "SalesOrderDetail": [
                {
                    "Product": {
                        "ProductID": 905,
                        "Name": "ML Mountain Frame-W - Silver, 42",
                        "ProductNumber": "FR-M63S-42"
                    },
                    "OrderQty": 4,
                    "UnitPrice": "218.4540",
                    "LineTotal": "873.8160"
                },
                ...
            ]
        }
    ]
}

2. /customer-orders/<customer_id>

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "SalesOrderID": 71780,
            "OrderDate": "2008-06-01T00:00:00Z",
            "TotalDue": "42452.6519",
            "SalesOrderDetail": [
                {
                    "Product": {
                        "ProductID": 905,
                        "Name": "ML Mountain Frame-W - Silver, 42",
                        "ProductNumber": "FR-M63S-42"
                    },
                    "OrderQty": 4,
                    "UnitPrice": "218.4540",
                    "LineTotal": "873.8160"
                },
                ...
            ]
        }
    ]
}

3. /discounted-orders

{
    "count": 43,
    "next": "http://localhost:8000/discounted-orders?page=2",
    "previous": null,
    "results": [
        {
            "OrderDate": "2008-06-01T00:00:00Z",
            "TotalDue": "42452.6519",
            "SalesOrderDetail": [
                {
                    "Product": {
                        "ProductID": 905,
                        "Name": "ML Mountain Frame-W - Silver, 42",
                        "ProductNumber": "FR-M63S-42"
                    },
                    "OrderQty": 4,
                    "UnitPrice": "218.4540",
                    "LineTotal": "873.8160"
                },
                {
                    "Product": {
                        "ProductID": 983,
                        "Name": "Mountain-400-W Silver, 46",
                        "ProductNumber": "BK-M38S-46"
                    },
                    "OrderQty": 2,
                    "UnitPrice": "461.6940",
                    "LineTotal": "923.3880"
                },
                ...
            ]
        },
        ...
    ]
}


---------------------------------------------------

Pagination:

Default page size: 5

Query params: page_size, page_number

---------------------------------------------------

Running the service:

Dependencies:

pip install django
pip install djangorestframework
pip install request
pip install pytest
pip install jsonschema

To start the server:

python manage.py runserver

The server start at localhost:8000

---------------------------------------------------

Running the tests: 

In order to run the tests:
1. Start the python server using python manage.py runserver
2. Make the following installations:
    pip install pytest
    pip install jsonschema
3. Switch to the tests directory
4. Run pytest
