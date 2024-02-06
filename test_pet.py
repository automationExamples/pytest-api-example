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

'''
QA_NOTE: Empty records returned for "sold" status but it is returning 200. 
Not sure may be the expectation is to validate what status available for users
'''


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 200
    for res in response.json():
        validate(instance=res, schema=schemas.pet)
        assert res["status"] == status


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''


'''
QA OBSERVATION: The test is passing for "a_str" as path. 
Not sure but seems it need a different status, may be 400
'''


@pytest.mark.parametrize("pet_id", [3, 4, "a_str"])
def test_get_by_id_404(pet_id):
    test_endpoint = "/pets/{}".format(pet_id)

    response = api_helpers.get_api_data(test_endpoint)
    assert response.status_code == 404
