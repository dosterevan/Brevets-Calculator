"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import logging
import requests # The library we use to send requests to the API
# Not to be confused with flask.request.
import arrow
import flask
from flask import request
import acp_times  # Brevet time calculations
import logging

# Set up Flask app
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

##################################################
################### API Callers ################## 
##################################################

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

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
    begin = request.args.get("begin_date", "now", type=str)
    distance = request.args.get("distance", 999, type=float)
    open_time = acp_times.open_time(km, distance, arrow.get(begin)).format('YYYY-MM-DDTHH:mm:ss')
    close_time = acp_times.close_time(km, distance, arrow.get(begin)).format('YYYY-MM-DDTHH:mm:ss')
    if 1.2*distance < km:
        result = {"failure": False}
        return flask.jsonify(result=result)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


def get_times():
    """
    Obtains the newest document in the "lists" collection in database
    by calling the RESTful API.

    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = requests.get(f"{API_URL}brevets").json()

    # lists should be a list of dictionaries.
    # we just need the last one:
    brevet = lists[-1]
    #app.logger.debug("form_data: %s", form_data_list)  
    return brevet["distance"], brevet["begin_date"], brevet["controls"]

"""# Iterate through the list of documents
for data in form_data_list:
    # Check if the required keys are present in the document
    if all(key in data for key in ["distance", "begin_date", "controls"]):
        return data["distance"], data["begin_date"], data["controls"]
    else:
        app.logger.debug("Missing key in data: %s", data) """
    


def insert_times(distance, begin_date, controls):
    
    """ Inserts brevet distance, control distance(s), open times, and close times into the database "brevetsdb", under the collection "times".
    
    Inputs brevet_distance (string), control_distances (list of strings), open_times (list of strings), and close_times (list of strings)

    Returns the unique ID assigned to the document by mongo (primary key.)"""
    
    # Log the output
    #app.logger.debug("output = ", output)

    # Get the unique ID assigned to the inserted document
    #_id = requests.post(f"{API_URL}/brevets", json = {"distance": distance, "begin_date": begin_date, "controls": controls}).json()
    #app.logger.debug("_id", _id)

    response = requests.post(f"{API_URL}brevets", json={"distance": distance, "begin_date": begin_date, "controls": controls})
    print(response.text)  # Print the raw server response
    _id = response.json()   


    # Return the ID 
    return _id


@app.route('/insert', methods=['POST'])
def insert():
    try:
        # Parse the JSON data from the request
        input_json = request.json
        #app.logger.debug(input_json)

        # Extract data from the JSON
        distance = input_json["distance"]
        #app.logger.debug(distance)
        begin_date = input_json["begin_date"]
        #app.logger.debug("controls = %s", input_json["controls"])
        controls = input_json["controls"]


        # Insert data into the database
        app.logger.debug("insert times = %s", insert_times(distance, begin_date, controls))
        time_id = insert_times(distance, begin_date, controls)
        #app.logger.debug("time_id = %s", time_id)

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


@app.route("/fetch")
def fetch():
    """  
    
    fetch : fetches the brevet distance, control distance(s), open times, and close times from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON"""
 
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

if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")