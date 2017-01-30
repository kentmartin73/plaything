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

def pp_json(data):
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

client = Elasticsearch()



server_api_key = sys.argv[1]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def incoming():
    have_error = False
    client_api_key = request.args.get("api_key")
    sensor_name = request.args.get("sensor_name")
    sensor_value = request.args.get("sensor_value")
    #if client_api_key != server_api_key:
    #    content = {'invalid api key': 'please enter a valid one'}
    #    return content, status.HTTP_401_UNAUTHORIZED
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
            float(sensor_value)
        except ValueError:
            error_content += "sensor_value is not a number\n"
            have_error = True

    if have_error:
        sys.stderr.write(error_content)
        sys.stderr.flush()
        return error_content, status.HTTP_417_EXPECTATION_FAILED

    if client_api_key != server_api_key:
        error_content = "API key invalid\n"
        return error_content, status.HTTP_401_UNAUTHORIZED

    # Build something to store
    id =  int(time.time())
    when = datetime.datetime.utcnow().isoformat()
    store_me = {}
    store_me['when'] = when
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
