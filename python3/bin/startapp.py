import os
import traceback
from flask import Flask, request, make_response
from Utils.loggerhandler import mylogger
from Utils.staticfile import ai_static_file
from stencil import py_demo

import json


app = Flask(__name__)

# prepare logger
log_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'log' + os.path.sep + 'startapp.log'
logger = mylogger(os.path.splitext(os.path.basename(__file__))[0], log_path)

app.register_blueprint(py_demo)
app.register_blueprint(ai_static_file)


@app.before_request
def before_request():
    logger.info('request %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, json.dumps(request.json, ensure_ascii=False, indent=2))


@app.after_request
def after_request(response):
    if request.blueprint == 'ai_static_file':
        logger.info('response static file %s' , request.path)
    else:
        logger.info('response %s %s %s %s %s %s' , request.remote_addr , request.method , request.scheme , request.full_path ,
            response.status , response.data)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    logger.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', request.remote_addr, request.method, request.scheme, request.full_path, tb)
    return e.message


if __name__ == '__main__':
    # start app
    # app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=True)
