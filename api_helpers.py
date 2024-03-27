import requests

base_url = 'http://127.0.0.1:5000'

# GET requests
def get_api_data(endpoint, params = {}):
    response = requests.get(f'{base_url}{endpoint}', params=params)
    return response

# POST requests
def post_api_data(endpoint, data):
    response = requests.post(f'{base_url}{endpoint}', json=data)
    return response

# PATCH requests
def patch_api_data(endpoint, data):
    response = requests.patch(f'{base_url}{endpoint}', json=data)
    return response