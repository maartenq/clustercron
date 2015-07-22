"""
Tests for `clustercron` module.
"""

from __future__ import print_function
from __future__ import unicode_literals
import pytest
from clustercron import elb


class Inst_health_state(object):
    def __init__(self, instance_id, state):
        self.instance_id = instance_id
        self.state = state


def test_Elb_constants():
    '''
    Test constances of Elb class.
    '''
    assert elb.Elb.URL_INSTANCE_ID == \
        'http://169.254.169.254/1.0/meta-data/instance-id'


def test_Elb_init():
    '''
    Test Elb attributes set by __init__.
    '''
    elb_lb = elb.Elb('mylbname')
    assert elb_lb.__dict__ == {'lb_name': 'mylbname'}


def test_Elb_get_inst_health_states(monkeypatch):
    '''
    Test Elb _get_inst_health_states method.
    '''
    pass


@pytest.mark.parametrize('instance_id,inst_health_states,is_master', [
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        True,
    ),
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        True,
    ),
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'Anything'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        True,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        False,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        False,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'anything'},
        ],
        True,
    ),
    (
        None,
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        False,
    ),
    (
        None,
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        False,
    ),
])
def test_elb_is_master(instance_id, inst_health_states, is_master):
    print(instance_id, inst_health_states, is_master)
    elb_lb = elb.Elb('mylbname')
    assert elb_lb._is_master(
        instance_id,
        [Inst_health_state(**x) for x in inst_health_states]) == is_master
