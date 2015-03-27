"""
Tests for `clustercron` module.
"""

from clustercron import clustercron


class Test_OptArgParser():
    def test_init(self):
        opt_arg_parser = clustercron.OptArgParser([])
        assert opt_arg_parser.arg_list == []
        assert opt_arg_parser.exitcode == 3
        assert opt_arg_parser.args == {
            'version': False,
            'help': False,
            'verbose': False,
            'dry_run': False,
            'lb_type': None,
            'lb_instance': None,
            'command': [],
        }
