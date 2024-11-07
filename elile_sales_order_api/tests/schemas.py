order_details_schema = {
    "type": "object",
    "properties": {
        "count": {"type": "number"},
        "next": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        },
        "previous": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        },
        "results": {
            "type": "array",
            "items": {
                "Customer": {
                    "type": "object",
                    "properties": {
                        "CustomerID": {"type": "number"},
                        "FirstName": {"type": "string"},
                        "LastName": {"type": "string"},
                        "EmailAddress": {"type": "string"},
                        "Phone": {"type": "string"}
                    }             
                },
                "OrderDate": {"type": "string"},
                "TotalDue": {"type": "number"},
                "Product": {
                    "type": "object",
                    "properties": {
                        "ProductID": {"type": "number"},
                        "Name": {"type": "string"},
                        "ProductNumber": {"type": "string"}
                    }
                },
                "SalesOrderDetail": {
                    "type": "object",
                    "properties": {
                        "QrderQty": {"type": "number"},
                        "UnitPrice": {"type": "number"},
                        "LineTotal": {"type": "number"}
                    }
                },
                "ShipToAddress": {
                    "type": "object",
                    "properties": {
                        "AddressLine1": {"type": "string"},
                        "AddressLine2": {"type": "string"},
                        "City": {"type": "string"},
                        "PostalCode": {"type": "string"}
                    }
                },
                "BillToAddress": {
                    "type": "object",
                    "properties": {
                        "AddressLine1": {"type": "string"},
                        "AddressLine2": {"type": "string"},
                        "City": {"type": "string"},
                        "PostalCode": {"type": "string"}
                    }
                }
            }
        }
    }
}

customer_orders_schema = {
    "type": "object",
    "properties": {
        "count": {"type": "number"},
        "next": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        },
        "previous": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        },
        "results": {
            "type": "array",
            "items": {
                "SalesOrderID": {"type": "number"},
                "OrderDate": {"type": "string"},
                "TotalDue": {"type": "float"},
                "Product": {
                    "type": "object",
                    "properties": {
                        "ProductID": {"type": "number"},
                        "Name": {"type": "string"},
                        "ProductNumber": {"type": "string"}
                    }
                }
            }
        }
    }
}

discounted_orders_schema = {
    "type": "object",
    "properties": {
        "count": {"type": "number"},
        "next": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        },
        "previous": {
            "anyOf": [
                {"type": "string"},
                {"type": "null"},
            ]
        },
        "results": {
            "type": "array",
            "properties": {
                "OrderDate": {"type": "string"},
                "TotalDue": {"type": "number"},
                "Product": {
                    "type": "object",
                    "properties": {
                        "ProductID": {"type": "number"},
                        "Name":  {"type": "string"},
                        "ProductNumber": {"type": "string"}
                    }
                }
            }
        }
    }
}