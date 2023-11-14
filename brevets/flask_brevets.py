"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
import os

from pymongo import MongoClient

###
# Globals
###

app = flask.Flask(__name__)
CONFIG = config.configuration()

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

db = client.brevets

collection = db.lists


##################################################
################ MongoDB Functions ############### 
##################################################

def get_brevet():

    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    controls = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for control in controls:
        
        return control["brevet"], control["controls"]


def submit_brevet(brevet, controls):

    output = collection.insert_one({
        "brevet": brevet, # the length of the whole brevet
        "controls": controls}) # I think controls will also be a dictionary
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    
    return str(_id)


##################################################
################## Flask routes ################## 
##################################################

###
# Pages
###

@app.route("/submit", methods=["POST"])
def submit():

    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        brevet = input_json["brevet"] # Should be a string
        controls = input_json["controls"] # Should be a list of dictionaries

        brevet_id = submit_brevet(brevet, controls)

        return flask.jsonify(result={},
                        message="Submitted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brevet_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Server error!", 
                        status=0, 
                        mongo_id='None')


@app.route("/display")
def display():

    try:
        brevet, controls = get_brevet()
        return flask.jsonify(
                result={"brevet": brevet, "controls": controls}, 
                status=1,
                message="Successful Display.")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't display brevets.")





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
@app.get("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    control_dist = request.args.get('control', None, type=float)
    start_time = request.args.get('start', None, type=arrow.get)
    brevet_dist = request.args.get('brevet', None, type=int)


    app.logger.debug(f"control={control_dist}")
    app.logger.debug(f"request.args: {request.args}")

    open_time = acp_times.open_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    return {"open": open_time, "close": close_time}

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
