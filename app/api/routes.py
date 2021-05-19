import collections
from flask import (Blueprint,
                    request,
                    jsonify)
from app import mongo

api = Blueprint('api',__name__)

@api.route('/')
def home():
    results = mongo.hub.list_collection_names()

    return(jsonify(status = 'connected', collections=results,Manhattan=restaurants))

@api.route('/filter', methods=['GET'])
def api_filter():
    query_parameters = request.args.to_dict()

    return query_parameters