"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""
#Check if given distance is greater than session distance

import nose    # Testing framework
from nose.tools import assert_equal
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import acp_times
import arrow
from pymongo import MongoClient
import flask
from flask_brevets import get_times, insert_times


app = flask.Flask(__name__)

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

"""
Brevet distance = 200km
"""

def test_200km():
     brevet_start_time = arrow.get("2022-01-01T00:00:00")
     brevet_dist_km = 200
     
     # Test Case 1
     control_dist_km = 60
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "01:46")
     nose.tools.assert_equal(close_time.format("HH:mm"), "04:00")

     # Test Case 2
     control_dist_km = 120
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "03:32")
     nose.tools.assert_equal(close_time.format("HH:mm"), "08:00")

     #Test Case 3
     control_dist_km = 175
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "05:09")
     nose.tools.assert_equal(close_time.format("HH:mm"), "11:40")

     #Test Case 3
     control_dist_km = 200
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "05:52")
     nose.tools.assert_equal(close_time.format("HH:mm"), "13:30")

def test_600km():
     brevet_start_time = arrow.get("2022-01-01T00:00:00")
     brevet_dist_km = 600

     # Test Case 1: Control at 100km
     control_dist_km = 100
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "02:56")
     nose.tools.assert_equal(close_time.format("HH:mm"), "06:40")

     # Test Case 2: Control at 200km
     control_dist_km = 200
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "05:53")
     nose.tools.assert_equal(close_time.format("HH:mm"), "13:20")

     # Test Case 3: Control at 350km
     control_dist_km = 350
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "10:34")
     nose.tools.assert_equal(close_time.format("HH:mm"), "23:20")

def test_550():
     brevet_start_time = arrow.get("2022-01-01T00:00:00")
     brevet_dist_km = 600

     # Test Case 1: Control at 550km
     control_dist_km = 550
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "17:08")
     nose.tools.assert_equal(close_time.format("DDD HH:mm"), "2 12:40") # this is the same as saying 36:40, it includes the first day

def test_600():
     brevet_start_time = arrow.get("2022-01-01T00:00:00")
     brevet_dist_km = 600

     # Test Case 1: Control at 600km (end of brevet)
     control_dist_km = 600
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("HH:mm"), "18:48")
     nose.tools.assert_equal(close_time.format("DDD HH:mm"), "2 16:00") # this is the same as saying 40:00, it includes the first day

def test_890():
     brevet_start_time = arrow.get("2022-01-01T00:00:00")
     brevet_dist_km = 1000

     # Test Case 1: Control at 890km 
     control_dist_km = 890
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("DDD HH:mm"), "2 05:09")
     nose.tools.assert_equal(close_time.format("DDD HH:mm"), "3 17:22")


def test_1000km():
     brevet_start_time = arrow.get("2022-01-01T00:00:00")
     brevet_dist_km = 1000

     # Test Case 1: Control at 1000km (end of brevet) 
     control_dist_km = 1000
     open_time = acp_times.open_time(control_dist_km, brevet_dist_km, brevet_start_time)
     close_time = acp_times.close_time(control_dist_km, brevet_dist_km, brevet_start_time)
     nose.tools.assert_equal(open_time.format("DDD HH:mm"), "2 09:05")
     nose.tools.assert_equal(close_time.format("DDD HH:mm"), "4 03:00")


if __name__ == '__main__':
    nose.runmodule()
