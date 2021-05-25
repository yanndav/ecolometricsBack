import collections
from dns.rdatatype import NULL
from flask import (Blueprint,
                    request,
                    jsonify,
                    abort,
                    render_template)
from app import mongo, mail
import re
from datetime import datetime
from flask_mail import Message
from app.api.functions import checkEmail
from app.api.functions import oecdAPI as oecd

api = Blueprint('api',__name__)

@api.route('/')
def home():
    results = mongo.db.list_collection_names()

    return(jsonify(status = 'connected_to_api', collections=results))

@api.route('/getDim', methods=['GET'])
def api_dimensions():
    # Retrieving user's request
    query_parameters = request.args.to_dict()

    # Dimensions:
    dim = {
        '_id':0,
        "location.name":1,
        "variable.name":1,
        "source":1,
        "category":1}

    search = {}
    if 'source' in query_parameters.keys():
        src = query_parameters['source']
        src_re = re.compile(src, re.IGNORECASE)
        search['source'] = src_re

    if 'variable' in query_parameters.keys():
        var = query_parameters['variable']
        var_re = re.compile(var, re.IGNORECASE)
        search['variable.name']=var_re
    
    if 'location' in query_parameters.keys():
        loc = query_parameters['location']
        loc_re = re.compile(loc, re.IGNORECASE)
        search['location.name'] = loc_re

    if 'category' in query_parameters.keys():
        cat = query_parameters['category']
        cat_re = re.compile(cat, re.IGNORECASE)
        search['category'] = cat_re

    results = list(mongo.db["structure"].find(search, dim))
    return(jsonify(results))

@api.route('/getData', methods=['GET'])
def api_filter():
    # Retrieving user's request
    query_parameters = request.args.to_dict()

    # Getting user's request parameters
    search = {}
    dim = {
        '_id':0
    }
    if 'variable' in query_parameters.keys():
        var = query_parameters['variable']
        var_re = re.compile(var, re.IGNORECASE)
        search['variable.name']=var_re
    
    if 'location' in query_parameters.keys():
        loc = query_parameters['location']
        loc_re = re.compile(loc, re.IGNORECASE)
        search['location.name'] = loc_re
    
    results = list(mongo.db["structure"].find(search,dim).limit(1))[0]

    if results['source']=="OECD":
        data = oecd.oecdOutput(
            results['dataSet'],
            results['variable'],
            results['location']
        )
        return(jsonify(data))

    else:
        return "Error"
    
    # return(jsonify(results))
    

@api.route('/earlyAccess', methods=['POST'])
def get_mail():
    if not request.args or not 'email' in request.args:
        return(jsonify(status="Please send valid args post format"),400)
    
    # Email
    email = request.args['email']

    if not checkEmail(email):
        return(jsonify(status="Email format not valid"),400)

    # Initialisation early_access db
    earlyAccess = mongo.db['early_access']
    # Date of access
    date = datetime.now()
    
    

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
            subject='[Accès anticipé] Ecolometrics ✅',
            recipients=[email],
            sender=('Ecolometrics','ecolometricsapp@gmail.com'),
            body=render_template("mail/earlyAccess.txt"),
            html=render_template("mail/earlyAccess.html")
            )
            

        mail.send(msg)

    return(jsonify(status="Succesfully added"),201)


