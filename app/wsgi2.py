import flask
from flask import request, jsonify
import os
import json
import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dirPath = os.getcwd()

# Create some test data for our catalog in the form of a list of dictionaries.
with open(os.path.join(dirPath,"testData","database.json"),'r') as base:
    data = json.load(base)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Just an ugly API</h1>
<p>Things will be improved shortly.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(data)



# A route for testing filtering

@app.route('/api/filter', methods=['GET'])
def api_filter():
    query_parameters = request.args.to_dict()

    return query_parameters


app.run()