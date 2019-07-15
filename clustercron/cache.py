# clustercron/cache.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.cache
-----------------
'''

import fcntl
import io
import json
import logging
import logging.handlers
import time
import random

from datetime import datetime
from datetime import timedelta


LOGGER = logging.getLogger(__name__)


class Cache():
    def __init__(self):
        self.master = False
        self.dct = {
            'master': self.master,
            'isodate': datetime(1970, 1, 1)
        }

    @staticmethod
    def json_serial(obj):
        '''
        JSON serializer for objects not serializable by default json code
        '''
        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    @staticmethod
    def iso2datetime_hook(dct):
        dct['isodate'] = datetime.strptime(
            dct['isodate'], '%Y-%m-%dT%H:%M:%S.%f')
        return dct

    def set_now(self):
        self.dct = {
            'master': self.master,
            'isodate': datetime.now(),
        }

    def load_json(self, fd):
        self.dct = json.load(fd, object_hook=self.iso2datetime_hook)
        self.master = self.dct['master']

    def safe_json(self, fd):
        fd.write(
            json.dumps(
                self.dct,
                default=self.json_serial,
                ensure_ascii=False,
            )
        )

    def expired(self, expire_time):
        return datetime.now() - self.dct['isodate'] > \
            timedelta(seconds=int(expire_time))


def check(master_check, filename, expire_time, max_iter):
    cache = Cache()
    for i in range(int(max_iter)):
        file_exists = False
        retry = False
        time.sleep(random.random())
        try:
            LOGGER.debug('Open cache file for read/write (try %s).', i + 1)
            fd = io.open(filename, 'r+')
            file_exists = True
        except IOError as error:
            if error.errno != 2:
                raise
            LOGGER.debug('No cache file. Open new cache file for write.')
            fd = io.open(filename, 'w')
        try:
            LOGGER.debug('Lock cache file.')
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as error:
            if error.errno != 11:
                raise
            LOGGER.debug('Cache file is locked.')
            retry = True
        else:
            if file_exists:
                LOGGER.debug('Read cache from existing file.')
                cache.load_json(fd)
                if cache.expired(expire_time):
                    LOGGER.debug('Cache expired, do check.')
                    cache.master = master_check()
                    cache.set_now()
                    LOGGER.debug('Write cache to existing file.')
                    fd.seek(0)
                    cache.safe_json(fd)
                    fd.truncate()
                else:
                    LOGGER.debug('Cache not expired.')
            else:
                LOGGER.debug('Do check.')
                cache.master = master_check()
                cache.set_now()
                LOGGER.debug('Write cache to new file.')
                cache.safe_json(fd)
        finally:
            LOGGER.debug('Unlock cache file.')
            fcntl.flock(fd, fcntl.LOCK_UN)
            LOGGER.debug('Close cache file.')
            fd.close()
        if retry:
            LOGGER.debug('Sleep 1 second before retry.')
            time.sleep(1)
            continue
        else:
            break
    LOGGER.debug('Is master: %s,', cache.master)
    return cache.master
