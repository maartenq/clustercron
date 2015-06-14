# clustercron/elb.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.elb
---------------
'''

from __future__ import unicode_literals

import logging
import socket
import boto.ec2.elb

from .compat import PY3

if PY3:
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.error import URLError

else:
    from urllib2 import Request
    from urllib2 import urlopen
    from urllib2 import URLError


logger = logging.getLogger(__name__)


class Elb(object):
    URL_INSTANCE_ID = \
        'http://169.254.169.254/1.0/meta-data/instance-id'
    ERRNO_NOT_MASTER = 1
    ERRNO_UNABLE_TO_GET_INSTANCE_ID = 2
    ERRNO_UNABLE_TO_GET_HEALTH_STATE = 4

    def __init__(self, lb_name, errno=0,  timeout=3):
        self.lb_name = lb_name
        self.errno = errno
        socket.setdefaulttimeout(timeout)

    def _get_instance_id(self):
        request = Request(self.URL_INSTANCE_ID)
        logger.debug('Get instance ID from URL: %s', self.URL_INSTANCE_ID)
        try:
            response = urlopen(request)
        except URLError as error:
            self.errno += self.ERRNO_UNABLE_TO_GET_INSTANCE_ID
            logger.debug('Failed to get instance ID: %s', error)
            instance_id = None
        else:
            instance_id = response.read()[:10]
        return instance_id

    def _get_inst_health_states(self):
        logger.debug('Get instance health state')
        try:
            conn = boto.ec2.elb.ELBConnection()
            lb = conn.get_all_load_balancers(
                load_balancer_names=[self.lb_name])[0]
            inst_health_states = lb.get_instance_health()
        except Exception as error:
            logger.debug('Failed to get instance health state: %s', error)
            self.errno += self.ERRNO_UNABLE_TO_GET_HEALTH_STATE
            inst_health_states = []
        return inst_health_states

    def _check_master(self, instance_id, inst_health_states):
        instances_in_service = [
            x.instance_id for x in inst_health_states
            if x.state == 'InService'
        ]
        if instances_in_service:
            instances_in_service.sort()
            if instance_id != instances_in_service[0]:
                self.errno += self.ERRNO_NOT_MASTER

    def check_master(self):
        instance_id = self._get_instance_id()
        if instance_id:
            inst_health_states = self._get_inst_health_states(self)
            self._check_master(instance_id, inst_health_states)
