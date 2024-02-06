
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


'''
Fixture get_order: checks for status as available exist,
 if not then creates one unique id having satus as available for test
'''

@pytest.fixture()
def get_order():
    test_endpoint = "/pets/findByStatus"
    place_order_endpoint = "/store/order"
    params = {
        "status": "available"
    }
    response = api_helpers.get_api_data(test_endpoint, params)
    if len(response.json()) == 0:
        pet_id_list = [pet_obj["id"] for pet_obj in api_helpers.get_api_data("/pets/").json()]
        new_pet_id = max(pet_id_list) + 3
        new_pet_data = {
            "id": new_pet_id,
            "name": "Luna",
            "type": "cat",
            "status": "available"
        }
        response = api_helpers.post_api_data("/pets/", new_pet_data)

    pet_id = iter(response.json()).__next__()["id"]
    data = {
        "pet_id": pet_id
    }
    order_response = api_helpers.post_api_data(place_order_endpoint, data)
    return order_response.json()


@pytest.mark.parametrize("status", ["sold"])
def test_patch_order_by_id(get_order, status):
    order = get_order
    validate(instance=order, schema=schemas.order)
    order_id, pet_id = order["id"], order["pet_id"]

    patch_endpoint = "/store/order/{}".format(order_id)

    data = {
        "status": status
    }

    patch_response = api_helpers.patch_api_data(patch_endpoint, data)

    assert patch_response.status_code == 200 and \
           patch_response.json()["message"] == "Order and pet status updated successfully"

    #   validating from /pets/pet_id endpoint if status changed to sold
    test_endpoint = "/pets/{}".format(pet_id)
    response = api_helpers.get_api_data(test_endpoint)
    assert response.json()["status"] == status
