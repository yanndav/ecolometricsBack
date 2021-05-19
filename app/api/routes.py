from flask import (render_template,
                    url_for, 
                    redirect,
                    Blueprint,
                    request,
                    jsonify)


api = Blueprint('api',__name__)

@api.route('/')
def home():
    return(render_template('api.html'))

@api.route('/filter', methods=['GET'])
def api_filter():
    query_parameters = request.args.to_dict()

    return query_parameters