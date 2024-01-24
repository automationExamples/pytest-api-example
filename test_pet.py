from jsonschema import validate
import pytest
import schemas
import api_helpers
import json
from hamcrest import assert_that, contains_string, is_


def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)


@pytest.mark.parametrize("status", [("pending"),("available")])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }
    expected_status = status
    response = api_helpers.get_api_data(test_endpoint, params)
    assert response.status_code == 200
    response_data = response.json()
    for pet_info in response_data:
        actual_status = pet_info.get('status')
        assert actual_status == expected_status, f"Expected status: {expected_status}, Actual status: {actual_status}"
   
    # Validate the schema for each object in the response
    for pet_info in response_data:
         validate(instance=pet_info, schema=schemas.pet)



@pytest.mark.parametrize("ids", [("8928627"),("*"),("-1000001")])
def test_get_by_id_404(ids):
    # TODO...
    test_endpoint = "/pets/" + ids
    response = api_helpers.get_api_data(test_endpoint)
    assert response.status_code == 404

    pass