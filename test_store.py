from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture
def create_payload():
   return {"pet_id": 0}

@pytest.fixture
def update_payload():
   return {"status": "available"}

def test_patch_order_by_id(create_payload, update_payload):

    # Create an order
    test_endpoint = "/store/order"
    response = api_helpers.post_api_data(test_endpoint, create_payload)

    # Validate the order schema
    assert response.status_code == 201
    if response.status_code == 201:
        validate(response.json(), schemas.order)

    order_id = response.json().get('id')

    test_endpoint = "/store/order/" + order_id
    response = api_helpers.patch_api_data(test_endpoint, update_payload)

    assert response.status_code == 200
    assert response.json().get("message") == 'Order and pet status updated successfully'
    pass