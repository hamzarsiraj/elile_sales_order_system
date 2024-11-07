import json
import jsonschema
import jsonschema.exceptions
from jsonschema import validate
import requests
from schemas import order_details_schema, customer_orders_schema, discounted_orders_schema
from elile_sales_order_system.settings import DEFAULT_PAGE_SIZE, SERVER

def test_orderdetails_validorderid_success():
    url = SERVER + "/order-details/71780"

    response = requests.request("GET", url)

    assert response.status_code == 200

def test_orderdetails_pageinfonotspecified_returnsdefaultsize():
    url = SERVER + "/order-details/71780"

    response = requests.request("GET", url)
    dict = json.loads(json.dumps(response.json()))

    assert len(dict["results"]) <= DEFAULT_PAGE_SIZE

def test_orderdetails_specifypageinfo_success():
    url = SERVER + "/order-details/71780?page_size=3&page_number=1"

    response = requests.request("GET", url)
    dict = json.loads(json.dumps(response.json()))

    assert len(dict["results"]) == 3

def test_orderdetails_nonexistentorderid_notfound():
    url = SERVER + "/order-details/0"

    response = requests.request("GET", url)

    assert response.status_code == 404

def test_orderdetails_validateschema():
    url = SERVER + "/order-details/71780"

    response = requests.request("GET", url)
    dict = json.dumps(response.json()) 

    assert is_valid_schema(json.loads(dict), order_details_schema) == True

def test_orderdetails_invalidorderid_notfound():
    url = SERVER + "/order-details/abc"

    response = requests.request("GET", url)

    assert response.status_code == 404

def test_customerorders_validcustomerid_success():
    url = SERVER + "/customer-orders/30113"

    response = requests.request("GET", url)

    assert response.status_code == 200

def test_customerorders_pageinfonotspecified_returnsdefaultsize():
    url = SERVER + "/customer-orders/30113"

    response = requests.request("GET", url)
    dict = json.loads(json.dumps(response.json()))

    assert len(dict["results"]) <= DEFAULT_PAGE_SIZE

def test_orderdetails_specifypageinfo_success():
    url = SERVER + "/customer-orders/30113?page_size=3&page_number=1"

    response = requests.request("GET", url)
    dict = json.loads(json.dumps(response.json()))

    assert len(dict["results"]) <= 3

def test_customerorders_nonexistentcustomerid_notfound():
    url = SERVER + "/customer-orders/0"

    response = requests.request("GET", url)

    assert response.status_code == 404

def test_customerorders_validateschema():
    url = SERVER + "/customer-orders/30113"

    response = requests.request("GET", url)
    dict = json.dumps(response.json())

    assert is_valid_schema(json.loads(dict), customer_orders_schema) == True

def test_customerorders_invalidorderid_notfound():
    url = SERVER + "/customer-orders/abc"

    response = requests.request("GET", url)

    assert response.status_code == 404

def test_discountedorders_success():
    url = SERVER + "/discounted-orders"

    response = requests.request("GET", url)

    assert response.status_code == 200

def test_discountedorders_validateschema():
    url = SERVER + "/discounted-orders"

    response = requests.request("GET", url)
    dict = json.dumps(response.json())

    assert is_valid_schema(json.loads(dict), discounted_orders_schema) == True

def is_valid_schema(jsonData, schema):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True
    