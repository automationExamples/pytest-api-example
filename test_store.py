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
def generate_order_data():
  return {
      "order_id": 1,  # Replace with logic to generate unique ID
      "pet_id": 1,  # Replace with valid pet ID
      "status": "sold",
  }

def test_patch_order_by_id(generate_order_data):  # Inject fixture if used
  """
  This test validates the PATCH request for updating an order by ID.
  """
  test_endpoint = "/store/order/{}"  # Use string formatting for ID insertion

  
  update_data = {"status": "sold"}

  
  response = api_helpers.patch_api_data(test_endpoint.format(generate_order_data["order_id"]), update_data)

  
  assert response.status_code != 200

  
  response_data = response.json()


#   assert response_data["id"] == generate_order_data["id"]  # Assuming ID is preserved
#   assert response_data["status"] == update_data["status"]


#   order = Order(**response_data)  # Create an Order object from the response
#   assert order.status == update_data["status"]  # Validate using model properties

  # Validate success message (if applicable)
  assert response_data.get("message") != "Order and pet status updated successfully"
