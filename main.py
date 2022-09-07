from http import HTTPStatus
from flask import Flask, Response, request, make_response
from GeoService import *

app = Flask(__name__)


# 127.0.0.1:5000/?addr=63, Большая Морская
@app.route("/", methods=['GET'])
def root_get():
    service = GeoService()

    service_response: Address = service.get_coord_by_address(
        request.args.get('addr')
    )

    response: Response = make_response(
        json.dumps(service_response, cls=AddressEncoder),
        HTTPStatus.OK)

    response.headers['Content-Type'] = "application/json; charset=UTF-8"

    return response


# {
#     "addr": [
#         "Большая Морская, 29",
#         "Санкт-Петербург, Большая морская, 29",
#         "Большая морская"
#     ]
# }

@app.route("/", methods=['POST'])
def root_post():
    service = GeoService()

    print('json = ', request.get_json())

    responses = []
    for addr in request.get_json()['addr']:
        print('addr =', addr)
        responses.append(service.get_coord_by_address(addr))

    response: Response = make_response(
        json.dumps(responses, cls=AddressEncoder),
        HTTPStatus.OK)

    response.headers['Content-Type'] = "application/json; charset=UTF-8"

    return response


if __name__ == '__main__':
    app.run(debug=True)
