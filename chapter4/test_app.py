import pytest
from apistar import test
from app import app, airports, AIRPORT_NOT_FOUND

client = test.TestClient(app)

@pytest.fixture
def correct_response_fixture():
    return {
        "id": 1, "airport_name": "Imperial Municipal Airport",
        "continent_code": "NA", "country_code": "US", "municipality": "Imperial",
        "gps_code": "KIML", "elevation": 3275
    }

@pytest.fixture
def airport_not_found_fixture():
    return {'error': AIRPORT_NOT_FOUND}

def test_list_all_airports(correct_response_fixture):
    response = client.get('/')
    assert response.status_code == 200

    json_resp = response.json()
    count_aps = len(json_resp)
    assert count_aps == len(airports)
    assert json_resp[0] == correct_response_fixture

@pytest.mark.parametrize('id,expected_response', [
    (1, 'correct_response_fixture'),
    (7777, 'airport_not_found_fixture')
])
def test_get_airport(id, expected_response, request):
    if id == 1:
        response = client.get(f'/{id}')
        json_resp = response.json()
        assert json_resp == request.getfixturevalue(expected_response)
    if id == 7777:
        response = client.get(f'/{id}')
        print(response)
        assert response.status_code == 404
        assert response.json() == request.getfixturevalue(expected_response)


