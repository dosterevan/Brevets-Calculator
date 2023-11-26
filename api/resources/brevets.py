"""
Resource: BrevetsResource
"""
from flask import Response, request
from flask_restful import Resource
import logging
from dateutil import parser

from database.models import Brevet, Checkpoint


class BrevetsResource(Resource):
    def get(self):
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        input_json = request.json
        input_json['begin_date'] = parser.parse(input_json['begin_date'])
        result = Brevet(**input_json).save()
        return {'_id': str(result.id)}, 200
