import collections
from dns.rdatatype import NULL
from flask import (Blueprint,
                    request,
                    jsonify)
from app import mongo
import json
from bson import json_util

api = Blueprint('api',__name__)

@api.route('/')
def home():
    results = mongo.db.list_collection_names()

    return(jsonify(status = 'connected_to_api', collections=results))

@api.route('/getData', methods=['GET'])
def api_filter():
    # Retrieving user's request
    query_parameters = request.args.to_dict()

    # Dimensions:
    dim = {'variable':1,'location':1,'values':1,'_id':0}

    # Getting user's request parameters
    # Collection 
    col = query_parameters['collection']
    # If searching for variable
    search = {}
    if 'variable' in query_parameters.keys():
        var = query_parameters['variable']
        search['variable'] = {"$gte":var}
    
    if 'location' in query_parameters.keys():
        loc = query_parameters['location']
        search['location'] = {"$gte":loc}

    results = list(mongo.db[col].find(search, dim))
    return json.dumps(results, default=json_util.default)
    # return jsonify(search)

@api.route('/getVariable', methods=['GET'])
def api_variables():
    # Retrieving user's request
    query_parameters = request.args.to_dict()

