import io
import os

from .loggerhandler import mylogger


class loadconf():
    def __init__(self, config_path):
        rootdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = rootdir + os.path.sep + 'log' + os.path.sep + os.path.splitext(os.path.basename(__file__))[
            0] + '.log'
        if not hasattr(self,'logger'):
            self.logger = mylogger(os.path.splitext(os.path.basename(__file__))[0], log_path)
        self.path = config_path
        self.config = self.load()

    def load(self):
        config = dict()
        if os.path.exists(self.path):
            self.logger.info('load file: %s', self.path)
            with io.open(self.path, 'rt', newline='\n') as cf:
                for line in cf:
                    splits = line.strip().split('=')
                    if not line.startswith('#') and len(splits) > 1:
                        cf_key = splits[0]
                        cf_value = splits[1]
                        config[cf_key] = cf_value
                        self.logger.info('%s = %s', cf_key, cf_value)
                    else:
                        self.logger.info('skip line: %s', line.strip())
        else:
            self.logger.info('file does not exist: %s', self.path)
        return config
