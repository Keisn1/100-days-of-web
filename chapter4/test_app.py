import pytest
from apistar import test
from app import app, airports, AIRPORT_NOT_FOUND

client = test.TestClient(app)

@pytest.fixture
def correct_response_fixture():
    return {"id": 1,
            "airport_name": "Imperial Municipal Airport",
            "continent_code": "NA",
            "country_code": "US",
            "municipality": "Imperial",
            "gps_code": "KIML",
            "elevation": 3275
            }

@pytest.fixture
def create_airport_fixture():
    return {'id': '123',
            'airport_name': 'Flughafen Innsbruck',
            'continent_code': 'EU',
            'country_code': 'AT',
            'municipality': 'Tirol',
            'gps_code': 'INNS',
            'elevation': 5000
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

@pytest.mark.parametrize('test_input', [
    ('create_airport_fixture')
])
def test_create_airport(test_input, request):
    num_aps = len(airports)
    new_ap = request.getfixturevalue(test_input)
    response = client.post('/', data=new_ap)
    assert response.status_code == 201
    new_ap["id"] = num_aps + 1
    assert response.json() == new_ap
    assert len(airports) == num_aps + 1

    response = client.get(f'/{num_aps + 1}')
    assert response.status_code == 200
    assert response.json() == new_ap

@pytest.mark.parametrize('test_input', [
    ('correct_response_fixture')
])
def test_create_airport_after_delete(test_input, request):
    correct_airport = request.getfixturevalue(test_input)
    id = correct_airport["id"]
    ap_count = len(airports)
    response = client.delete(f'/{id}')
    assert response.status_code == 204
    assert len(airports) == ap_count - 1

    response = client.post('/', data=correct_airport)
    assert response.status_code == 201
    assert len(airports) == ap_count

def test_create_airport_missing_fields():
    data = {'key': 1}
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors['airport_name'] == 'The "airport_name" field is required.'
    assert errors['continent_code'] == 'The "continent_code" field is required.'
    assert errors['country_code'] == 'The "country_code" field is required.'
    assert errors['municipality'] == 'The "municipality" field is required.'
    assert errors['gps_code'] == 'The "gps_code" field is required.'
    assert errors['elevation'] == 'The "elevation" field is required.'

def test_create_car_validation():
    data = {
        "continent_code": "UN",
        "country_code": "QQ",
        "elevation": -10000
    }
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert "Must be one of" in errors['continent_code']
    assert "Must be one of" in errors['country_code']
    assert errors['elevation'] == 'Must be greater than or equal to -2000.'


def test_airport_not_found():
    response = client.get('/11111')
    assert response.status_code == 404
    assert response.json() == {'error': AIRPORT_NOT_FOUND}

