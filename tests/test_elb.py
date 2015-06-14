"""
Tests for `clustercron` module.
"""

from __future__ import print_function

import mock
import pytest
from clustercron import elb


def test_Elb_init():
    elb_lb = elb.Elb('mylbname')
    assert elb_lb.lb_name == 'mylbname'
    assert elb_lb.errno == 0


@pytest.mark.parametrize('instance_id,inst_health_states,errno', [
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        0,
    ),
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        0,
    ),
    (
        u'i-1d564f5c',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'Anything'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        0,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        1,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
        ],
        1,
    ),
    (
        u'i-cba0ce84',
        [
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
            {'instance_id': u'i-1d564f5c', 'state': u'anything'},
        ],
        0,
    ),
    (
        None,
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        1,
    ),
    (
        None,
        [
            {'instance_id': u'i-1d564f5c', 'state': u'InService'},
            {'instance_id': u'i-cba0ce84', 'state': u'InService'},
        ],
        1,
    ),
])
def test_elb__check_master(instance_id, inst_health_states, errno):
    print(instance_id, inst_health_states, errno)
    elb_lb = elb.Elb('mylbname')
    elb_lb._check_master(
        instance_id, [mock.Mock(**x) for x in inst_health_states]
    )
    assert elb_lb.errno == errno
