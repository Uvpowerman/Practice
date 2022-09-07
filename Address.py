import json


class Address:
    id: int
    country: str
    city: str
    street: str
    housenumber: str
    lon: float
    lat: float

    def __init__(self, *args):
        self.id, self.country, self.city, self.street, \
        self.housenumber, self.lon, self.lat = args

        self.id = int(self.id)
        self.lon = round(float(self.lon), 6)
        self.lat = round(float(self.lat), 6)


class AddressEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Address):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def addressDecoder(obj):
    if 'country' and 'city' and 'street' and \
            'housenumber' and 'lon' and 'lat' in obj.keys():

        return Address(-1,
                       obj.get('country'),
                       obj.get('city'),
                       obj.get('street'),
                       obj.get('housenumber'),
                       obj.get('lon'),
                       obj.get('lat'))

    else:
        return obj
