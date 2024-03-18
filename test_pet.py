from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''

def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)
    print(f'output value: {response}')
    # print(schemas.pet)

    assert response.status_code == 200

            
    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
# @pytest.mark.parametrize("status", [("available")])
@pytest.mark.parametrize("status", [("available"), ('sold'), ("pending")])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)    
    print(f'response code: {response.status_code}')
    print(f'response status: {response}')
    assert response.status_code == 200  
    
    # assert response.json()["status"] == status
    for pet in response.json():
        assert pet["status"] == status
        validate(instance=pet, schema=schemas.pet) 

'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
def test_get_by_id_404():
    test_endpoint = "/pets/5"
    response = api_helpers.get_api_data(test_endpoint)

  # Assert a 404 status code for non-existent pet
    assert response.status_code == 404
