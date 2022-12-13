from typing import Dict, List
import json

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def _load_airport_data() -> Dict:
    with open("airport_data.json") as file_:
        airport_data = json.load(file_)
        airports = {}
        for ap in airport_data:
            if not ap["elevation"]:
                continue
            ap["elevation"] = int(ap["elevation"])

            if not ap["municipality"]:
                continue
            if not ap["gps_code"]:
                continue

            ap["id"] = len(airports) + 1
            airports[ap["id"]] = ap
    return airports

airports = _load_airport_data()
VALID_CONTINENT_CODES = set([ap["continent_code"]for ap in airports.values()])
VALID_COUNTRY_CODES = set([ap["country_code"] for ap in airports.values()])
all_elevation = set([ap["elevation"] for ap in airports.values()])
AIRPORT_NOT_FOUND = "Airport not found"
AIRPORT_ALREADY_EXISTS = "Airport is already in the database"


class Airport(types.Type):
    id = validators.Integer(allow_null=True)
    airport_name = validators.String(max_length=100)
    continent_code = validators.String(enum=list(VALID_CONTINENT_CODES))
    country_code = validators.String(enum=list(VALID_COUNTRY_CODES))
    municipality = validators.String(max_length=100)
    gps_code = validators.String(max_length=4)
    elevation = validators.Integer(minimum=-2000, maximum=20000)


def list_all_airports() -> List[Airport]:
    return [Airport(ap) for ap in airports.values()]

def get_airport(ap_id: int) -> JSONResponse:
    ap = airports.get(ap_id)
    if not ap:
        error = {'error': AIRPORT_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(ap, status_code=200)

def create_airport(ap: Airport):
    # ap.id = len(airports.keys()) + 1 this would not work once you add and delete airports - setting new ap to an id always present
    ap.id = max(airports.keys()) + 1
    ap_names = set([ap["airport_name"] for ap in airports.values()])
    if ap.airport_name in ap_names:
        error = {'error': AIRPORT_ALREADY_EXISTS}
        return JSONResponse(error, status_code=409)

    airports[ap.id] = Airport(ap)
    return JSONResponse(Airport(ap), status_code=201)

def update_airport(ap_id: int, ap: Airport):
    if ap_id not in airports.keys():
        error = {'error': AIRPORT_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    ap.id = ap_id
    airports[ap_id] = ap
    return JSONResponse(Airport(ap), status_code=200)


def delete_airport(ap_id: int):
    if ap_id not in airports.keys():
        error = {'error': AIRPORT_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    del airports[ap_id]
    return JSONResponse({}, status_code=204)

routes = [
    Route('/', method="GET", handler=list_all_airports),
    Route('/', method="POST", handler=create_airport),
    Route('/{ap_id}', method="GET", handler=get_airport),
    Route('/{ap_id}', method="PUT", handler=update_airport),
    Route('/{ap_id}', method="DELETE", handler=delete_airport)
]

app = App(routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
