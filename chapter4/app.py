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

            airports[ap["id"]] = ap

    return airports

airports = _load_airport_data()
VALID_CONTINENT_CODES = set([ap["continent_code"]for ap in airports.values()])
VALID_COUNTRY_CODES = set([ap["country_code"] for ap in airports.values()])
all_elevation = set([ap["elevation"] for ap in airports.values()])
AIRPORT_NOT_FOUND = "Airport not found"

class Airport(types.Type):
    id = validators.Integer(allow_null=True)
    airport_name = validators.String(max_length=100)
    continent_code = validators.String(max_length=2)
    country_code = validators.String(max_length=2)
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

    return JSONResponse(Airport(ap), status_code=200)

routes = [
    Route('/', method="GET", handler=list_all_airports),
    Route('/{ap_id}', method="GET", handler=get_airport)
]

app = App(routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
