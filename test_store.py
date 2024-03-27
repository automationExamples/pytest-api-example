from jsonschema import validate
import pytest
import schemas
import json
import random
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
def get_random_pet_ids():
    pet_id_set = [0, 1, 2]
    pet_id = random.choice(pet_id_set)
    print("pet_id-->", pet_id)
    return pet_id


def post_an_order_to_get_pet(pet_id):
  test_endpoint = "/store/order"
  data = {
     "pet_id": pet_id
     } 
  response = api_helpers.post_api_data(test_endpoint, data)
  print("post_api_data_response", response)
  assert response.status_code == 201
  if response.status_code == 201:
        validate(response.json(), schemas.order)
  order_id = response.json().get('id')
  return order_id


# function to test the PATCH request /store/order/{order_id}
def test_patch_order_by_id(get_random_pet_ids):
    pet_id = get_random_pet_ids # get the random pet ids through fixture
    print("pet_id",pet_id) 
    # Get the order id from the post operation
    order_id = post_an_order_to_get_pet(pet_id)
    print("post_order_response", order_id)
    # concatenate order id to patch url
    test_endpoint = "/store/order/" + order_id
    data = {
        "status": "available"
        } 
    response = api_helpers.patch_api_data(test_endpoint, data)
    assert response.status_code == 200
    assert response.json().get("message") == 'Order and pet status updated successfully'
    