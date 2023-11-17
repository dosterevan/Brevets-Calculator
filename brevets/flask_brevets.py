"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config as config
import os
from pymongo import MongoClient

# Set up MongoDB connection
#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

import logging

###
# Globals
###
app = flask.Flask(__name__)
#CONFIG = config.configuration()

# Set up Flask app#
app.debug = True
app.logger.setLevel(logging.DEBUG)


# Use database "brevets"
db = client.brevets

# Use collection of "times" in the database
times = db.lists

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    brevet_dist = request.args.get('distance')
    brevet_dist = float(brevet_dist)
    app.logger.debug(brevet_dist)
    #control_dist = request.form['control_dist']
    #app.logger.debug(print("control_dist="), control_dist)
    
    start_time_str = request.args.get('begin_date')
    start_time = arrow.get(start_time_str)
    
    open_time = acp_times.open_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')

    close_time = acp_times.close_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')

    if 1.2*brevet_dist < km:
        result = {"failure": brevet_dist < km}
        return flask.jsonify(result=result)

    result = {"open": open_time, "close": close_time, }
    return flask.jsonify(result=result)


def get_times():
    """
    Obtains the newest document in the "lists" collection in the database "brevets".

    Returns title (string) and items (list of dictionaries) as a tuple.
    """

    # Retrieve the latest document from the "times" collection
    form_data = times.find().sort("_id", -1).limit(1)
    
    # Convert the Cursor to a list
    form_data_list = list(form_data)  
    
    # Log the retrieved list
    app.logger.debug("form_data: %s", form_data_list)  

    # Iterate through the list of documents
    for data in form_data_list:
        # Check if the required keys are present in the document
        if all(key in data for key in ["distance", "begin_date", "controls"]):
            return data["distance"], data["begin_date"], data["controls"]
        else:
            app.logger.debug("Missing key in data: %s", data)
    

@app.route('/insert', methods=['POST'])
def insert():
    try:
        # Parse the JSON data from the request
        input_json = request.json

        # Extract data from the JSON
        distance = input_json["distance"]
        begin_date = input_json["begin_date"]
        controls = input_json["controls"]

        # Insert data into the database
        time_id = insert_times(distance, begin_date, controls)
        app.logger.debug("time_id = %s", time_id)

        # Respond with a JSON message indicating success
        return flask.jsonify(result={},
                             message="Inserted!",
                             status=1,
                             mongo_id=time_id)
    except Exception as e:
        app.logger.debug("Oh no! Server error! Exception: %s", str(e))

        # Respond with a JSON message indicating failure
        return flask.jsonify(result={},
                             message="Oh no! Server error!",
                             status=0,
                             mongo_id='None')
    

def insert_times(distance, begin_date, controls):
    """
    Inserts brevet distance, control distance(s), open times, and close times into the database "brevetsdb", under the collection "times".
    
    Inputs brevet_distance (string), control_distances (list of strings), open_times (list of strings), and close_times (list of strings)

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    
    # Insert data into the "times" collection
    output = times.insert_one({
        "distance": distance,
        "begin_date": begin_date,
        "controls": controls})
    
    # Log the output
    #app.logger.debug("output = ", output)

    # Get the unique ID assigned to the inserted document
    _id = output.inserted_id
    
    # Return the ID as a string
    return str(_id)


@app.route("/fetch")
def fetch():
    """
    /fetch : fetches the brevet distance, control distance(s), open times, and close times from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Get the latest data from the database
        distance, begin_date, controls = get_times()  

        # Check if any of the required data is missing
        if distance is None or begin_date is None or controls is None:
            app.logger.debug("get_times returned None")

            # Respond with a JSON message indicating failure
            return flask.jsonify(
                result={}, 
                status=0,
                message="Failed to fetch data!")
        
        app.logger.debug("fetched!")

        # Log the fetched data
        app.logger.debug("distance = %s", distance)  
        app.logger.debug("begin_date = %s", begin_date)
        app.logger.debug("controls = %s", controls)

        # Respond with a JSON message indicating success
        return flask.jsonify(
                result={"distance": distance, "begin_date": begin_date, "controls": controls}, 
                status=1,
                message="Successfully fetched all data!")
    except Exception as e:
        app.logger.debug("Exception occurred: %s", str(e))

        # Respond with a JSON message indicating failure
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any times/distances!")

    

#############

#app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    #print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=5000, host="0.0.0.0")