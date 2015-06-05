# clustercron/elb.py
# vim: ts=4 et sw=4 sts=4 ft=python fenc=UTF-8 ai
# -*- coding: utf-8 -*-

'''
clustercron.elb
----------------------
'''

from __future__ import unicode_literals

import logging
import socket
import urllib2

from .exceptions import UnableToGetEC2InstanceIdException

# general libary logging
logger = logging.getLogger(__name__)

SOCKET_TIMEOUT = 10
URL_INSTANCE_ID = 'http://169.254.169.254/latest/meta-data/instance-id'


socket.setdefaulttimeout(SOCKET_TIMEOUT)


class Elb(object):
    def __init__(self, lb_name):
        self.lb_name = lb_name
        self.instance_id = None

    def get_instance_id(self):
        request = urllib2.Request(URL_INSTANCE_ID)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            raise UnableToGetEC2InstanceIdException
        return response

#import boto
#import boto.ec2.elb
#conn = boto.ec2.elb.ELBConnection()
#conn.get_all_load_balancers(load_balancer_names=['<name>']
#i = a.instances[0]
#i.id
