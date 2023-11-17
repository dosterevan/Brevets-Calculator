"""
Nose tests for Mongo DB 

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
from nose.tools import assert_equal
from pymongo import MongoClient
import flask
import logging
from flask_brevets import get_times, insert_times

app = flask.Flask(__name__)

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


# Fetch test
def test_fetch():
    # Can only accurately test for begin_date
    distance_check = '300'
    begin_date_check = "2021-01-01T00:00"
    km_check = 0
    open_check = "2021-01-01T00:00"
    close_check = "2021-01-01T01:00"
    result = get_times()
    print("got em!")
    nose.tools.assert_equal(result[0], distance_check)
    nose.tools.assert_equal(result[1], begin_date_check)
    nose.tools.assert_equal(result[2][0]["km"], km_check)
    nose.tools.assert_equal(result[2][0]["open"], open_check)
    nose.tools.assert_equal(result[2][0]["close"], close_check)


# Insert test
def test_insert():
     # Can only accurately test for begin_date
     distance = '300'
     begin_date = "2021-01-01T00:00"
     controls = [{"km": 0, "open": "2021-01-01T00:00", "close": "2021-01-01T01:00"}]
     _id = insert_times(distance, begin_date, controls)

     nose.tools.assert_is_instance(_id, str)