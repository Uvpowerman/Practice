from sqlalchemy import create_engine, and_, or_, text
import sqlalchemy as db
import psycopg2
import json
import requests
from requests.structures import CaseInsensitiveDict
import re

from Address import *


class GeoService:
    engine = create_engine("postgresql+psycopg2://postgres:uvpowerman@localhost/map")
    connection = engine.connect()
    map = db.Table('addr', db.MetaData(),
                   autoload=True,
                   autoload_with=engine)
    response_limit = 1000

    # filter1 = False
    # filter2 = False
    # filter3 = True

    def get_coord_by_address(self, address: str):
        if address in ['', ' ', None]:
            return []

        print("regex =" + address_to_regex(address))

        query = db.select([self.map])

        # if (self.filter1):
        #     query_country = db.select([self.map.columns.id]).where(
        #         self.map.columns.country.regexp_like(
        #             address_to_regex(address)))
        #
        #     query_city = db.select([self.map.columns.id]).where(
        #         self.map.columns.city.regexp_like(
        #             address_to_regex(address)))
        #
        #     query_street = db.select([self.map.columns.id]).where(
        #         self.map.columns.street.regexp_like(
        #             address_to_regex(address)))
        #
        #     query_housenumber = db.select([self.map.columns.id]).where(
        #         self.map.columns.housenumber.regexp_like(
        #             address_to_regex(address)))
        #
        #     query = query.filter(or_(
        #         self.map.columns.id.in_(query_country),
        #         self.map.columns.country == None))
        #
        #     query = query.filter(or_(
        #         self.map.columns.id.in_(query_city),
        #         self.map.columns.city == None))
        #
        #     query = query.filter(self.map.columns.id.in_(query_street))
        #
        #     query = query.filter(or_(
        #         self.map.columns.id.in_(query_housenumber),
        #         self.map.columns.housenumber == None))
        #
        # if (self.filter2):
        #     query = query \
        #         .filter(text('street ~ :regexp')) \
        #         .params(regexp=address_to_regex(address)) \
        #         .filter(text('housenumber ~ :regexp')) \
        #         .params(regexp=address_to_regex(address))

        # if (self.filter3):
        request_api = False

        for t in ['street ~* :regexp', 'housenumber ~* :regexp',
                  'country ~* :regexp', 'city ~* :regexp']:
            new_query = query \
                .filter(text(t)) \
                .params(regexp=address_to_regex(address))
            if len(self.connection.execute(new_query).fetchall()) > 0:
                if t in ['street ~* :regexp', 'housenumber ~* :regexp']:
                    request_api = True
                query = new_query

        response = []
        for elem in self.connection.execute(query) \
                .fetchmany(self.response_limit):
            response.append(Address(*elem))

        if request_api:
            for i in get_from_api(address):
                response.append(i)

        return response


def address_to_regex(address: str):
    address = re.sub(re.compile(r' '), '.*', address)
    address = re.sub(re.compile(r','), '.*|', address)
    return '.*' + address + '.*'


def get_from_api(address: str):
    url = "https://api.geoapify.com/v1/geocode/search?text=" \
          + address + \
          "&apiKey=" \
          "5626b22bdfcb4f9fa88d69e510dfcdcc"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    response = json.loads(json.dumps(resp.json()), object_hook=addressDecoder)

    response = response.get('features')
    for i in range(len(response)):
        response[i] = response[i].get('properties')

    return response


