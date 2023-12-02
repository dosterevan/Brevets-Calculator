"""
Resource: BrevetResource
"""
from flask import Response, request
from flask_restful import Resource

from database.models import Brevet

class BrevetResource(Resource):
    def get(self, id):
        # Retrieve a Brevet object by its unique identifier and convert it to JSON format
        brevet = Brevet.objects.get(id=id).to_json()
        # Return the Brevet data as a JSON response with a 200 status code
        return Response(brevet, mimetype="application/json", status=200)

    def put(self, id):
        # Extract the JSON data from the incoming request
        input_json = request.json
        # Update the Brevet object with the provided data based on its unique identifier
        Brevet.objects.get(id=id).update(**input_json)
        # Return a success message with the updated Brevet's ID and a 200 status code
        return {'id': str(id), 'status': 'updated'}, 200

    def delete(self, id):
        # Delete the Brevet object identified by its unique identifier
        Brevet.objects.get(id=id).delete()
        # Return a success message with the deleted Brevet's ID and a 200 status code
        return {'id': str(id), 'status': 'deleted'}, 200
