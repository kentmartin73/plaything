#!/usr/bin/env python

import datetime
import json
import sys
from flask import Flask, request
from flask.ext.api import status

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import json
import time

#def pp_json(data):
#    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

client = Elasticsearch()

server_api_keys = sys.argv[1:]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def incoming():
    have_error = False
    client_api_key = request.args.get("a")
    sensor_name = request.args.get("n")
    sensor_value = request.args.get("v")

    error_content = ""
    if not client_api_key:
        sys.stderr.write("\n\n")
        sys.stderr.write(client_api_key)
        sys.stderr.write("\n\n")
        sys.stderr.flush()
        error_content += "Missing api_key\n"
        have_error = True
    if not sensor_name:
        sys.stderr.write("\n\n")
        sys.stderr.write(sensor_name)
        sys.stderr.write("\n\n")
        error_content += "Missing sensor_name\n"
        have_error = True
    if not sensor_value:
        sys.stderr.write("\n\n")
        sys.stderr.write(sensor_value)
        sys.stderr.write("\n\n")
        error_content += "Missing sensor_value\n"
        have_error = True
    else:
        try:
            sensor_value = float(sensor_value)
        except ValueError:
            error_content += "sensor_value is not a number\n"
            have_error = True

    if have_error:
        sys.stderr.write(error_content)
        sys.stderr.flush()
        return error_content, status.HTTP_417_EXPECTATION_FAILED

    if not client_api_key in server_api_keys:
        error_content = "API key invalid\n"
        return error_content, status.HTTP_401_UNAUTHORIZED

    if client_api_key == "vsk":
        customer = "Chess"
    else:
        customer = client_api_key

    # T1 = Boiler case temperature, it will get hot if central heating or hot water needs energy
    # T2 = Central heating output water temperature
    # T3 = Central heating radiator return water temperature
    # T4 = Mains water feed temperature (goes cold every time someone runs the water)
    # T5 = Room temp (affected by boiler so its the warmest room in the house)
    if sensor_name == "T1":
        sensor_name = "Boiler case"
    if sensor_name == "T2":
        sensor_name = "Central heating output"
    if sensor_name == "T3":
        sensor_name = "Central heating return"
    if sensor_name == "T4":
        sensor_name = "Mains feed"
    if sensor_name == "T5":
        sensor_name = "Room"

    sys.stderr.write(customer)
    sys.stderr.write(": ")
    sys.stderr.write(sensor_name)
    sys.stderr.write("\n")
    # Build something to store
    id =  int(time.time())
    when = datetime.datetime.utcnow().isoformat()
    store_me = {}
    store_me['when'] = when
    store_me['customer'] = customer
    store_me['sensor_name'] = sensor_name
    store_me['sensor_value'] = sensor_value
    #store_me_body = json.dumps(store_me)
    ##sys.stderr.write("\n")
    #sys.stderr.write(store_me_body)
    #sys.stderr.write("\n")
    client.index(
        index='incoming-sensors',
        doc_type = 'sensor_report',
        id = when,
        body = store_me
        #body = store_me_body
    )
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
