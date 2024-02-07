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
@pytest.fixture(params=[0,1,2])
def pet_id(request):
    return request.param

@pytest.mark.fixture_sample1
def test_get_order_id(pet_id):
   test_endpoint = "/store/order"
   payload={
        "pet_id": pet_id,
   }
   payload1={
   "status": "available",
   }
   get_order_id_response = api_helpers.post_api_data(test_endpoint,payload)
   if pet_id==1:
       print(f"The status code is: ",get_order_id_response.status_code)
       assert get_order_id_response.status_code==400
       assert get_order_id_response.json()["message"]=="Pet with ID 1 is not available for order"
   else:
       print(f"The status code is: ",get_order_id_response.status_code)
       assert get_order_id_response.status_code==201
       data=get_order_id_response.json()
       order_id=data["id"] 
       patch_order_id_response=api_helpers.patch_api_data(test_endpoint + f"/{order_id}",payload1)
       print(f"The status codes: ",patch_order_id_response.status_code)
       print(f"The response value: ",patch_order_id_response.json())
       assert patch_order_id_response.status_code==200
       assert patch_order_id_response.json()["message"]=="Order and pet status updated successfully"
