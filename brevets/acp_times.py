"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import flask
import logging



app = flask.Flask(__name__)


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# look at skeleton code, check if input value is greater than distance
# use assert statements
def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
      """
      Args:
         control_dist_km:  number, control distance in kilometers
            brevet_dist_km: number, nominal distance of the brevet
            in kilometers, which must be one of 200, 300, 400, 600, or 1000
            (the only official ACP brevet distances)
         brevet_start_time:  An arrow object
      Returns:
         An arrow object indicating the control close time.
         This will be in the same time zone as the brevet start time.
      """
      if control_dist_km < brevet_dist_km:   
         if control_dist_km <= 200:
            hours = control_dist_km / 33.9
         elif 200 < control_dist_km < 400:
            hours = 200 / 34 + (control_dist_km - 200) / 32 + 0.01
         elif 400 <= control_dist_km <= 600:
            hours = 200 / 34 + 200 / 32 + (control_dist_km - 400) / 30 + 0.01
         elif 600 < control_dist_km <= 1000:
            hours = 200 / 34 + 200 / 32 + 200 / 30 + (control_dist_km - 600) / 28 + 0.01
         #else: 
            #hours = 200 / 34 + 200 / 32 + 200 / 30 + 200 / 28 + (control_dist_km - 1000) / 26
      elif brevet_dist_km <= control_dist_km:
         if brevet_dist_km == 200 or brevet_dist_km == 300:
            hours = 200 / 34
         elif brevet_dist_km == 400:
            hours = 200 / 34 + (200) / 32 + 0.01
         elif brevet_dist_km == 600:
            hours = 200 / 34 + 200 / 32 + (200) / 29.95
        #elif brevet_dist_km == 1000:
            #hours = 200 / 34 + 200 / 32 + 200 / 30 + (200) / 28
         else: 
            hours = 33.09
      app.logger.debug(brevet_start_time.shift(hours=hours))
      return brevet_start_time.shift(hours=hours).format('YYYY-MM-DDTHH:mm:ss')     



def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
      """
      Args:
         control_dist_km:  number, control distance in kilometers
            brevet_dist_km: number, nominal distance of the brevet
            in kilometers, which must be one of 200, 300, 400, 600, or 1000
            (the only official ACP brevet distances)
         brevet_start_time:  An arrow object
      Returns:
         An arrow object indicating the control close time.
         This will be in the same time zone as the brevet start time.
      """
      if control_dist_km < brevet_dist_km:  
         if control_dist_km == 0:
            hours = 1
         elif 0 < control_dist_km < 600:
            hours = control_dist_km / 15 
         elif 600 <= control_dist_km <= 1000: 
            hours = 600 / 15 + (control_dist_km - 600) / 11.428
         elif control_dist_km > 1000:
            hours = 600 / 15 + 600 / 11.428 + (control_dist_km - 1200) / 13.333
      elif brevet_dist_km <= control_dist_km:
         if brevet_dist_km == 200:
            hours = 13.5
         elif brevet_dist_km <= 600:
            hours = brevet_dist_km / 15
         elif brevet_dist_km == 1000:
            hours = 600 / 15 + (400) / 11.428 + 0.01
         #elif brevet_dist_km > 1000:
            #hours = 600 / 15 + 1000 / 11.428 + (1200) / 13.333 + 0.01
      app.logger.debug(brevet_start_time.shift(hours=hours))
      return brevet_start_time.shift(hours=hours).format('YYYY-MM-DDTHH:mm:ss')  

