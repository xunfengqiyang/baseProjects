
import os
from flask import Flask, make_response,Blueprint
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from .loggerhandler import mylogger
import os.path


app = Flask(__name__)
ai_static_file = Blueprint('ai_static_file', __name__, template_folder='templates')


# define consts
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobname = os.path.splitext(os.path.basename(__file__))[0]

# prepare logger
log_path = rootdir + os.path.sep + 'log' + os.path.sep + jobname + '.log'
logger = mylogger(jobname, log_path)


path_seg = os.path.sep



def file_extension(path):
  return os.path.splitext(path)[1]


@ai_static_file.route('/static/<filename>')
def file_one(filename):
    base_dir = os.path.dirname(__file__)
    sub_dir = '..' + path_seg + 'static' + path_seg + filename
    src_dir = os.path.join(base_dir, sub_dir)
    resp = make_response(open(src_dir).read())
    resp.headers["Content-type"] = "application/json;charset=UTF-8"
    resp.headers['Cache-Control'] = "max-age=604800"
    resp.mimetype = 'application/javascript'
    return resp


@ai_static_file.route('/static/<subpath1>/<filename>')
def file_two(subpath1, filename):
    base_dir = os.path.dirname(__file__)
    sub_dir = '..' + path_seg + 'static' + path_seg + subpath1 + '/' + filename
    src_dir = os.path.join(base_dir, sub_dir)
    resp = make_response(open(src_dir).read())
    suffix = file_extension(filename)
    suffix = str(suffix)
    if suffix == ".css":
        resp.headers["Content-type"] = "text/css;charset=UTF-8"
    elif suffix == ".js":
        resp.headers["Content-type"] = "application/javascript;charset=UTF-8"
    resp.headers['Cache-Control'] = "max-age=604800"
    return resp

@ai_static_file.route('/static/<subpath1>/<subpath2>/<filename>')
def file_three(subpath1, subpath2, filename):
    base_dir = os.path.dirname(__file__)
    sub_dir = '..' + path_seg + 'static' + path_seg + subpath1 + '/' + subpath2 + '/' + filename
    src_dir = os.path.join(base_dir, sub_dir)
    resp = make_response(open(src_dir).read())
    if subpath2 == 'css':
        resp.headers["Content-type"] = "text/css;charset=UTF-8"
        resp.mimetype = 'text/css'
    if subpath2 == 'js':
        resp.headers["Content-type"] = "application/json;charset=UTF-8"
        resp.mimetype = 'application/javascript'
    resp.headers['Cache-Control'] = "max-age=604800"
    return resp


if __name__ == '__main__':
    # register blueprint
    app.register_blueprint(ai_static_file)

    app.run(host='0.0.0.0', port=8080, threaded=True)
    # app.run(host='localhost', port=8080, threaded=True)
    # app.run(host='10.116.128.109',port=8080,threaded=True)
    logger.info('......started......')