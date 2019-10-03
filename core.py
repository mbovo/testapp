from __future__ import absolute_import, division, print_function
import logging
import os
import time

logger = logging.getLogger(__name__)
LOG_LEVELS = {'CRITICAL': logging.CRITICAL, 'ERORR': logging.ERROR, 'WARNING': logging.WARNING, 'INFO': logging.INFO,
              'DEBUG': logging.DEBUG}

PROPERTIES = {
    'server': '',
    'port': '5000',
    'log_level': 'INFO',
    'stop_timeout': '1',
    'redis_host': "localhost",
    "redis_port": "6379",
    "app_version": "1.0.0"
}


class Config(object):
    """
        This is the main configuration class
        is thread safe 'cause you cannot write new values :)
    """

    def __init__(self):
        start = time.time()
        self.properties = {}
        for v in os.environ:
            if v.startswith('TESTAPP'):
                k = v.replace('TESTAPP', '').lower()
                if k in PROPERTIES:
                    PROPERTIES[k] = os.environ[v]
                else:
                    print("Unknown property: [{}]".format(k))

        for p in PROPERTIES:
            self.properties[p] = PROPERTIES[p]

        logging.basicConfig(
            format="%(asctime)s | %(process)5d |[%(threadName)10s] | %(levelname)9s | %(name)s:%(funcName)s() "
                   "| %(message)s",
            level=LOG_LEVELS[self.log_level.upper()])
        stop = time.time()
        logger.info('configuration loaded in ' + str(stop - start) + "s")

    def __iter__(self):
        for p in self.properties:
            yield p

    def __str__(self):
        return str(self.properties)

    def __getitem__(self, item):
        if item not in self.properties:
            raise KeyError
        return self.properties[item]

    def __getattr__(self, item):
        if item in self.properties:
            return self.properties[item]

