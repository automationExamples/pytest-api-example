from jsonschema import validate
import pytest
import schemas
import api_helpers
import json
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''


def test_patch_order_by_id(get_test_data):
    pet_id = get_test_data  # using Fixture getting random pet id
    print(pet_id)
    # placing order with required available pet id  and getting resonse of order id
    order_id = post_request(pet_id)
    # updating pet available status as ' pending '
    data = {'status': 'pending'}
    # response received for the patch update
    response = patch_request(order_id=order_id, data=data)
    assert response.status_code == 200  # validating response status as 200
    print(response.content)  # referce for response content
    order_message = json.loads((response.content).decode('utf8').replace(
        "'", '"'))  # converting binary content to validat json content
    # 4) Validate the response message "Order and pet status updated successfully"
    assert order_message.get(
        "message") == "Order and pet status updated successfully"

    # 2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
    # Required manual update in schemas.py file - i dont think its required in coding


# 1) Creating a function to test the PATCH request /store/order/{order_id}
def patch_request(order_id, data):
    test_endpoint = f"/store/order/{order_id}"
    order_status_message = api_helpers.patch_api_data(test_endpoint, data=data)
    return order_status_message


def post_request(pet_id):
    test_endpoint = f"/store/order"
    data = {}
    data["pet_id"] = pet_id
    print(data)
    # order_data,status_code = api_helpers.post_api_data(endpoint=test_endpoint, data=data)
    response = api_helpers.post_api_data(endpoint=test_endpoint, data=data)
    # 3) Validate the response codes and values
    assert response.status_code == 201
    print(response.content)
    order_data = json.loads(
        (response.content).decode('utf8').replace("'", '"'))
    order_id = order_data.get("id")
    print(order_id)
    return order_id


@pytest.fixture
def get_test_data():  # 2) *Optional* Consider using @pytest.fixture to create unique test data for each run
    import random
    pet_id_list = [0, 2]
    pet_id = random.choice(pet_id_list)
    return pet_id
