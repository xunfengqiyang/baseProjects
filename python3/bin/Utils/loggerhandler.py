# -*- coding: utf-8 -*-
# project: PycharmProjects
# file: loggerhandler
# author: gichen
# create time: 2018/6/7 4:23 PM
# product name: PyCharm
import logging
import os
import re
import sys
import time
from stat import ST_MTIME

try:
    import uwsgi

    uwsgi_mode = True
except:
    uwsgi_mode = False

# prepare env
from logging.handlers import TimedRotatingFileHandler


def check_version():
    if sys.version_info < (3, 0):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        sys.getfilesystemencoding = lambda: 'UTF-8'
        reload(sys)
    # else:
    #     sys.stdout.write('Please use python 2.x to run this script!\n')
    #     sys.exit(255)


check_version()

# basicConfig 打印library日志
logging.basicConfig(level=logging.INFO)
for hd in logging.getLogger().handlers:
    if isinstance(hd, logging.StreamHandler):
        hd.setLevel(20)


# make sure dir exist
def __makesuredirexist__(path):
    if not os.path.exists(path):
        sys.stdout.write('path does not exist: {}\n'.format(path))
        sys.stdout.write('auto create {}\n'.format(path))
        os.makedirs(path, 0o775)


class mylogger():
    def __init__(self, classname, log_path, when='midnight', interval=1, backupCount=0, level=10):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param classname:
        :param log_path:
        :param when:
        :param interval:
        :param backupCount:
        :param level: default DEBUG=10
        """
        # self attributes setting
        if uwsgi_mode:
            wk_id = uwsgi.worker_id()
            self.log_path = log_path + '.{}'.format(wk_id)
        else:
            self.log_path = log_path

        # 创建log文件父目录
        __makesuredirexist__(os.path.dirname(log_path))

        # 创建一个logger
        self.logger = logging.getLogger(classname)
        self.logger.setLevel(level)
        self.logger.propagate = 0

        # 创建一个handler，用于写入日志文件
        fh = TimedRotatingFileHandler(log_path, when=when, interval=interval, backupCount=backupCount, encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s - %(process)d] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        for hdlr in self.logger.handlers:
            self.logger.removeHandler(hdlr)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def _check_basefilename(self):
        """
        Only if uwsgi_mode is True, then check basefilename works.
        Aim to locate correct log file in case of multi processes.
        :return:
        """
        if uwsgi_mode:
            wk_id = uwsgi.worker_id()
            for h in self.logger.handlers:
                if isinstance(h, TimedRotatingFileHandler):
                    if h.baseFilename.endswith('.log'):
                        base_filename = h.baseFilename + '.{}'.format(wk_id)
                        h.baseFilename = base_filename
                        self.__reset_log_file(h)
                        continue
                    if re.match(r".*\.[0-9]", h.baseFilename) and not re.match(r".*\.{}".format(wk_id), h.baseFilename):
                        base_filename = '.'.join(h.baseFilename.split('.')[:-1]) + '.{}'.format(wk_id)
                        h.baseFilename = base_filename
                        self.__reset_log_file(h)
                        continue

    def __reset_log_file(self, handler):
        """
        change log file stream;
        change rolloverat
        re-open stream
        :param handler:
        :return:
        """
        if handler.stream:
            handler.stream.close()
            handler.stream = None
        if os.path.exists(handler.baseFilename):
            t = os.stat(handler.baseFilename)[ST_MTIME]
        else:
            t = int(time.time())
        handler.stream = handler._open()
        newRolloverAt = handler.computeRollover(t)
        while newRolloverAt <= t:
            newRolloverAt = newRolloverAt + handler.interval
        handler.rolloverAt = newRolloverAt

    def getlog(self):
        return self.logger

    def debug(self, msg, *args, **kwargs):
        self._check_basefilename()
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._check_basefilename()
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._check_basefilename()
        self.logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._check_basefilename()
        self.logger.warning(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._check_basefilename()
        self.logger.critical(msg, *args, **kwargs)
