from jsonschema import validate
import pytest
import schemas
import json
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
def create_test_order():
    return {"id": 1, "pet_id": 101}

def test_patch_order_by_id(create_test_order):
    
    id = create_test_order["id"]
    test_endpoint = f"/store/orders/{id}"
 
    existing_order = api_helpers.get_api_data(test_endpoint)
    print(f"Existing Order Details: {existing_order}")
    
    payload = {"status": "placed"}
    response = api_helpers.patch_api_data(test_endpoint, data=json.dumps(payload))

    assert response.status_code == 200, f"Expected 200 OK, but got {response.status_code}"

    updated_order = api_helpers.get_api_data(test_endpoint).json()

    expected_message = "Order and pet status updated successfully"
    assert response.json()["message"] == expected_message, f"Expected message: '{expected_message}'"

    assert updated_order["status"] == payload["status"], "Order status was not updated successfully"

    validate(instance=updated_order, schema=schemas.Order)