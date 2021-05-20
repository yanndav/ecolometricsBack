import collections
from dns.rdatatype import NULL
from flask import (Blueprint,
                    request,
                    jsonify,
                    abort)
from app import mongo, mail
import re
from datetime import datetime
from flask_mail import Message

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

@api.route('/earlyAccess', methods=['POST'])
def get_mail():
    if not request.json or not 'email' in request.json:
        return(jsonify(status="Please send email in valid format"),400)

    
    # Initialisation early_access db
    earlyAccess = mongo.db['early_access']
    # Date of access
    date = datetime.now()
    # Email
    email = request.json['email']

    # Searching for email existence in DB
    exists = earlyAccess.find_one({'email':email})

    if exists:
        return(jsonify(status="Already registered"),401)
    
    else:
        # Creating the document
        new_doc = {
            'email':email,
            'date':date}

        # Adding doc to dataset
        earlyAccess.insert_one(new_doc)
    
        msg = Message(
            subject='[Ecolometrics] Thank you for your interest!',
            recipients=[email],
            sender=('Ecolometrics','ecolometricsapp@gmail.com'),
            body='Hi,\n\nWe successfully added your email to our database and will keep in touch to inform you about the first release.\n\nBest,\nDavid Bros.'
        )

        mail.send(msg)

    return(jsonify(status="Succesfully added"),201)


