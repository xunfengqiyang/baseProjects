#python3
# -*- coding: utf-8 -*-
import os

import sys
from flask import Flask , Blueprint , request , render_template

from Utils.loggerhandler import mylogger
from Utils.loadconf import loadconf

# prepare logger


log_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'log' + os.path.sep + 'upload.log'
logger = mylogger(os.path.splitext(os.path.basename(__file__))[0], log_path)

rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobname = os.path.splitext(os.path.basename(__file__))[0]

# load conf
config_path = os.path.sep.join((rootdir, 'conf', jobname + '.conf'))
config_inside = loadconf(config_path).config


app = Flask(__name__, static_url_path='/static/')
py_demo = Blueprint('py_demo', __name__)


# try:
#     cur_conf_path = config_path + '.' + config_inside['cur_conf_path']
#     config = loadconf(cur_conf_path).config
# except Exception:
#     logger.error("Unexpected error: %s", sys.exc_info())
#     sys.exit(255)


@py_demo.before_request
def before_request():
    logger.debug('request %s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path,
                 request.json)


# @py_demo.route('/', defaults={'path': ''})
# @py_demo.route('/<path:path>')
# def index(path):
#     return render_template('index.html')


@py_demo.route('/')
def index():
#    return "<div>Hello world</div>"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)