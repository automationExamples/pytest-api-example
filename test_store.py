from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
import calendar
import time
import random
import json
import requests
import api_helpers

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

def patch_api_data(endpoint, data,path_variable):
    response = requests.patch(f'{api_helpers.base_url}{endpoint}/{path_variable}', json=data)
    return response

@pytest.fixture
def unique_pet_data():
    def generate_payload():
        # Generate a random name for the pet
        name = str(calendar.timegm(time.gmtime()))

        # Generate a random pet type
        pet_type = random.choice(["cat", "dog", "fish"])

        idValue = calendar.timegm(time.gmtime())
        payload =  {
            "id": idValue,
            "name": name,
            "type": pet_type,
            "status": "available"  
        }
        
        return json.dumps(payload)
    return generate_payload
    

def test_patch_order_by_id(unique_pet_data):
    
    test_endpoint = "/pets"
    payload = unique_pet_data()
    response = api_helpers.post_api_data(test_endpoint,json.loads(payload))
    
    assert response.status_code == 201
    payloadStr = json.loads(payload)
    pet_id = payloadStr["id"]
    assert response.json().get('id') == pet_id
    
    test_endpoint = "/store/order" 
    body = {
            "pet_id":pet_id
           }
    bodyStr = json.dumps(body)
    response = api_helpers.post_api_data(test_endpoint,json.loads(json.dumps(body)))
    assert response.status_code == 201
    validate(instance=response.json(), schema=schemas.order)

    getOrderId = response.json().get("id")
    test_endpoint = "/store/order"
    patch_payload = {
                        "status": "sold"
                    }
    patchStr = json.dumps(patch_payload)
   
    response = patch_api_data(test_endpoint,json.loads(patchStr),getOrderId)
    assert response.status_code == 200
    assert response.json().get('message') == "Order and pet status updated successfully"
    pass
