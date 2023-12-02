"""
Resource: BrevetsResource
"""
from flask import Response, request, Flask
from flask_restful import Resource
import logging
from datetime import datetime

from database.models import Brevet

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
    
class BrevetsResource(Resource):
    def get(self):
        # Retrieve all Brevet objects and convert them to JSON format
        json_object = Brevet.objects().to_json()
        # Return the Brevet data as a JSON response with a 200 status code
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Extract the JSON data from the incoming request
        input_json = request.json
        # Log the incoming JSON data for debugging purposes
        app.logger.debug(input_json)

        input_json["begin_date"] = datetime.strptime(input_json["begin_date"], '%Y-%m-%dT%H:%M')

        # Convert open and close times of all controls to datetime
        for control in input_json['controls']:
            control['open_time'] = datetime.strptime(control['open_time'], '%Y-%m-%dT%H:%M')
            control['close_time'] = datetime.strptime(control['close_time'], '%Y-%m-%dT%H:%M')

        # Create a new Brevet object with the provided data and save it to the database
        result = Brevet(**input_json).save()
        # Log the result of the save operation and specific attributes for debugging
        app.logger.debug(result)
        app.logger.debug(result["begin_date"])
        # Return the ID of the newly created Brevet object as part of the response with a 200 status code
        return {'_id': str(result.id)}, 200


