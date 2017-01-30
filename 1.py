#!/usr/bin/env python

import json
import sys
from flask import Flask, request
from flask.ext.api import status



server_api_key = sys.argv[1]
sys.stderr.write("Starting up")
sys.stderr.flush()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def incoming():
    got_params = True
    error_detail = {}
    error_detail['missing_keys'] = []
    client_api_key = request.args.get("api_key")
    sensor_name = request.args.get("sensor_name")
    sensor_value = request.args.get("sensor_value")
    #sensor_value = request.args.get("sensor_value")
    sys.stderr.write(str((client_api_key, sensor_name, sensor_value)))
    sys.stderr.flush()
    sys.stderr.write("\n\n*** got gets ***\n\n")
    sys.stderr.flush()
    if not client_api_key:
        error_detail['missing_keys'].append("api_key")
        got_params = False
    if not sensor_name:
        error_detail['missing_keys'].append("sensor_name")
        got_params = False
    if not sensor_value:
        error_detail['missing_keys'].append("sensor_value")
        got_params = False

    sys.stderr.write("\n\n *** After params\n\n")
    sys.stderr.write(str(got_params))
    sys.stderr.flush()
    if not got_params:
        sys.stderr.write("Param problem")
        content = json.dumps(error_detail)
        return content, status.HTTP_417_EXPECTATION_FAILED
    sys.stderr.write("\n\n *** After params 2\n\n")
    sys.stderr.flush()

#    if not isinstance(sensor_value, int):
#        content = { 'invalid value': 'sensor_value must be an int' }
#        return content, status.HTTP_417_EXPECTATION_FAILED
#    sys.stderr.write("\n\n *** After check sensor value\n\n")
#    sys.stderr.flush()
#    sys.stderr.write("\n\n *** client api key\n\n")
#    sys.stderr.write(client_api_key)
#    sys.stderr.write("\n\n *** client api key\n\n")
#    sys.stderr.flush()



#    if client_api_key != server_api_key:
#        content = {'invalid api key': 'please enter a valid one'}
#        return content, status.HTTP_401_UNAUTHORIZED
#    sys.stderr.write("\n\n *** After check api key\n\n")
#    sys.stderr.flush()

    print "Passed checks"
    return {'status': 'OK'}


if __name__ == '__main__':
    app.run(debug=True)
