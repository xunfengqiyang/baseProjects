import io
import os
import sys

from .loggerhandler import mylogger

__author__ = 'gichen'


# prepare env
def check_version():
    if sys.version_info < (3, 0):
        sys.stdout.write('Please use python 3.x to run this script!\n')
        sys.exit(255)


check_version()

# define consts
rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobname = os.path.splitext(os.path.basename(__file__))[0]
top_display = 18

# prepare logger
log_path = rootdir + os.path.sep + 'log' + os.path.sep + jobname + '.log'
logger = mylogger(jobname, log_path)


class loadfile():
    def __init__(self, file_path):
        self.file_path = file_path

    def as_dict(self, delimiter='='):
        result = dict()
        count = 0
        if os.path.exists(self.file_path):
            logger.info('load file: %s as dict', self.file_path)
            with io.open(self.file_path, 'rt', encoding='utf-8', newline='\n') as cf:
                for line in cf:
                    splits = line.strip().split(delimiter, 1)
                    if not line.startswith('#') and len(splits) > 1:
                        count += 1
                        cf_key = splits[0]
                        cf_value = splits[1]
                        result[cf_key] = cf_value
                        if count <= top_display:
                            logger.info('%s = %s', cf_key, cf_value)
                    else:
                        logger.info('skip line: %s', line.strip())
        else:
            logger.info('file does not exist: %s', self.file_path)
        return result

    def as_set(self):
        result = set()
        count = 0
        if os.path.exists(self.file_path):
            logger.info('load file: %s as set', self.file_path)
            with io.open(self.file_path, 'rt', encoding='utf-8', newline='\n') as cf:
                for line in cf:
                    if len(line.strip()) > 0:
                        count += 1
                        result.add(line.strip())
                        if count <= top_display:
                            logger.info('%s', line.strip())
                    elif len(line.strip()) > 0:
                        logger.info('skip line: %s', line.strip())
                    else:
                        pass
        else:
            logger.info('file does not exist: %s', self.file_path)
        return result

    def as_list(self):
        result = list()
        count = 0
        if os.path.exists(self.file_path):
            logger.info('load file: %s as list', self.file_path)
            with io.open(self.file_path, 'rt', encoding='utf-8', newline='\n') as cf:
                for line in cf:
                    if len(line.strip()) > 0:
                        count += 1
                        result.append(line.strip())
                        if count <= top_display:
                            logger.info('%s', line.strip())
                    elif len(line.strip()) > 0:
                        logger.info('skip line: %s', line.strip())
                    else:
                        pass
        else:
            logger.info('file does not exist: %s', self.file_path)
        return result


if __name__ == '__main__':
    l = loadfile('/workspace_pycharm/ai_api/data/stop_words.txt').as_list()
    print(l)
    s = loadfile('/workspace_pycharm/ai_api/data/stop_words.txt').as_set()
    print(s)
    d = loadfile('/workspace_pycharm/ai_api/data/stop_words.txt').as_dict()
    print(d)
    f = loadfile('/workspace_pycharm/ai_api/data/zh_fycs.txt').as_dict(' ')
    print(f)
