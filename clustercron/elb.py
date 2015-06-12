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
    ERRNO_UNABLE_TO_GET_INSTANCE_ID = 2
    ERRNO_UNABLE_TO_GET_HEALT_STATE = 4

    def __init__(self, lb_name, error_code=0,  timeout=3):
        self.lb_name = lb_name
        self.error_code = error_code
        socket.setdefaulttimeout(timeout)

    def get_instance_id(self):
        request = Request(self.URL_INSTANCE_ID)
        try:
            response = urlopen(request)
        except URLError:
            self.error_code += self.ERRNO_UNABLE_TO_GET_INSTANCE_ID
            instance_id = None
        else:
            instance_id = response.read()[:10]
        return instance_id

    def get_inst_health_states(self):
        try:
            conn = boto.ec2.elb.ELBConnection()
            lb = conn.get_all_load_balancers(
                load_balancer_names=[self.lb_name])[0]
            inst_health_states = lb.get_instance_health()
        except Exception as error:
            logger.debug(error)
            self.error_code += self.ERRNO_UNABLE_TO_GET_INSTANCE_ID
            inst_health_states = []
        return inst_health_states

    def get_instances(self, inst_health_states):
        self.instances = [x.instance_id for x in inst_health_states]
        self.instances_in_service = [
            x.instance_id for x in inst_health_states
            if x.state == 'InService'
        ]
        inst_health_states = ''
        self.instances.sort()
        self.instances_in_service.sort()

    @property
    def instances_in_service(self, inst_health_states):
        pass

    def _get_instances_ids_in_lb(self, loadbalancer):
        self.lb_instances_ids = [x.id for x in loadbalancer.instances]
        self.lb_instances_ids.sort()

    def _get_in_services_instances_ids_in_lb(self, loadbalancer):
        loadbalancer = \
            self.conn.get_all_load_balancers(
                load_balancer_names=[self.lb_name])[0]
        self.lb_instances_ids = [x.id for x in loadbalancer.instances]
        self.lb_instances_ids.sort()

    @property
    def instance_first_in_all_instances(self):
        self._get_loadbalancer(self.conn)
        if self.loadbalancer:
            self._get_instances_ids_in_lb(self.loadbalancer)
        if self.lb_instances_ids:
            return self.instance_id == self.lb_instances_id[0]
        else:
            return False

    @property
    def instance_first_in_all_instances(self):
        self._get_loadbalancer(self.conn)
        if self.loadbalancer:
            self._get_instances_ids_in_lb(self.loadbalancer)
        if self.lb_instances_ids:
            return self.instance_id == self.lb_instances_id[0]
        else:
            return False

    @property
    def instance_is_in_service(self):
        self.get_instance_id()
        self._get_instances_ids_in_lb()
        if self.lb_instances_ids:
            return self.instance_id == self.lb_instances_id[0]
        else:
            return False

    def get(self):
        pass
