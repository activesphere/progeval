from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from modules import rct
import random, json

# App Config
app = Flask(__name__)
CORS(app)

# Config Variables
app.config['MAX_CODE_LINES'] = 1000

# Response Wrappers
def _success_ok(data):
    return Response(response=data, status=200, content_type='application/json')

def _success_accepted(message='Accepted'):
    return Response(response=message, status=202, content_type='text/plain')

def _error_badrequest(message='Bad Request'):
    return Response(response=message, status=400, content_type='text/plain')

def _error_internalerr(message='Internal Server Error'):
    return Response(response=message, status=500, content_type='text/plain')

# Routes
@app.route('/evaluate', methods=['POST'])
def evaluate():
    req_data = request.get_json(silent=True)
  
    try:
        code_array = req_data.pop('code')
        lang = req_data.pop('lang')
        problem_id = req_data.pop('problem_id')
    except KeyError:
        return _error_badrequest()

    if len(code_array) > app.config.get('MAX_CODE_LINES'):
        return _error_badrequest()
   
    program_id = str(random.random()*10000000)
    lang = lang.upper()
  
    result = rct.run_at_scale(program_id, lang, code_array, problem_id)
    return _success_ok(json.dumps({'result': result }))

