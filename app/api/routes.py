import collections
from dns.rdatatype import NULL
from flask import (Blueprint,
                    request,
                    jsonify)
from app import mongo
import re

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
        var_re = re.compile(var, re.IGNORECASE)
        search['variable'] = var_re
    
    if 'location' in query_parameters.keys():
        loc = query_parameters['location']
        loc_re = re.compile(loc, re.IGNORECASE)
        search['location'] = loc_re

    results = list(mongo.db[col].find(search, dim))
    return jsonify(results)

@api.route('/getVariable', methods=['GET'])
def api_variables():
    # Retrieving user's request
    query_parameters = request.args.to_dict()

