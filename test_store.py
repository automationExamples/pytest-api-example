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
@pytest.mark.parametrize("order_id", ["1"])
def test_patch_order_by_id(order_id):
        
    patch_payload = {
        "status": "pending",
        "complete": True
    }

    response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_payload)

    try:
        assert response.status_code == 200

        assert_that(response.json().get("message"), is_("Order and pet status updated successfully"))

    except AssertionError as e:
        print(f"Test failed: {e}")
        raise  
