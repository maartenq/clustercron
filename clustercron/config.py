# clustercron/_CONFIG.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

import os.path
import configparser

_CONFIG = {
    'cache': {
        'filename': '/tmp/clustercron_cache.json',
        'expire_time': 59,
        'max_iter': 20,
    }
}


def _update_config_from_conf():
    basename = 'clustercron.ini'
    filenames = (
        os.path.join('/etc/', basename),
        os.path.join(os.path.expanduser("~"), '.' + basename)
    )
    parser = configparser.ConfigParser()
    for filename in filenames:
        if parser.read(filename) == [filename]:
            for section in parser.sections():
                try:
                    for key, value in parser.items(section):
                        try:
                            if _CONFIG[section].get(key, None) is not None:
                                _CONFIG[section][key] = value
                        except AttributeError:
                            break
                except configparser.NoSectionError:
                    pass


_update_config_from_conf()
for key, value in _CONFIG.items():
    globals()[key] = value
