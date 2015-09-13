Usage
=====

clustercron --help
------------------
::

    $ clustercron --help
    usage:
        clustercron [options] elb <loadbalancer_name> [<cron_command>]
        clustercron --version
        clustercron (-h|--help)

        options:
            (-v|--verbose)  Info logging. Add extra `-v` for debug logging.
            (-s|--syslog)   Log to (local) syslog.
            (-o|--output)   Output stdout and stderr from <cron_command>.

    Clustercron is cronjob wrapper that tries to ensure that a script gets run
    only once, on one host from a pool of nodes of a specified loadbalancer.

    Without specifying a <cron_command> clustercron will only check if the node
    is the `master` in the cluster and will return 0 if so.


Command line examples
---------------------

**Clustercron** can be run from command line for debugging.

**Clustercron** can be run with only *load balancer type* and *load balancer name*.
Without a *command* specified clustron will test is the node is *master* and
return 0 if that is the case::

    $ clustercron elb mylbname
    $ echo $?
    0

On one node::

    $ clustercron elb mylbname || echo "I'm not master"
    I'm not master

On other node::

    $ clustercron elb mylbname && echo "I'm master"
    I'm master


Check if node is master with verbose (info) output::

    $ clustercron -v elb mylbname
    INFO     clustercron.elb : Instance ID: i-ca289460
    INFO     clustercron.elb : All instances: i-58e224a1, i-ca289460 Instance in list: True
    INFO     clustercron.elb : Instances in service: i-58e224a1, i-ca289460 Instance in list: True
    INFO     clustercron.elb : This instance master: False


Check if node is master with verbose (info) output::

    $ clustercron -v elb mylbname
    INFO     clustercron.elb : Instance ID: i-ca289460
    INFO     clustercron.elb : All instances: i-58e224a1, i-ca289460 Instance in list: True
    INFO     clustercron.elb : Instances in service: i-ca289460 Instance in list: True
    INFO     clustercron.elb : This instance master: True


With options `-s`, `--syslog` and `-v`, `--verbose` **clustercron** will (only) output to syslog::

    $ clustercron -v -s elb clustercrontest echo test
    $ sudo tail  -9 /var/log/messages
    Sep 12 21:05:00 ip-172-30-0-83 requests.packages.urllib3.connectionpool [3871]: Starting new HTTP connection (1): 169.254.169.254
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.elb [3871]: Instance ID: i-58e224a1
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.elb [3871]: All instances: i-58e224a1, i-ca289460 Instance in list: True
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.elb [3871]: Instances in service: i-58e224a1, i-ca289460 Instance in list: True
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.elb [3871]: This instance master: True
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.main [3871]: run command: echo test
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.main [3871]: stdout: test
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.main [3871]: stderr:
    Sep 12 21:05:00 ip-172-30-0-83 clustercron.main [3871]: returncode: 0


By default **clustercron** does not output `stdout` or `stderr` of the 'cron-command'::

    $ clustercron elb clustercrontest echo test
    $


Output `stdout` or `stderr` of the 'cron-command' (while master)::

    $ clustercron -o elb clustercrontest echo test
    test

Normal redirect will work with options `-o`, `--output`:

    $ clustercron -o elb clustercrontest non-existing-command 2>/tmp/error
    $ cat /tmp/error


Cron entry example
------------------

Every day at 5 min to midnight run the command `logger "clustercron run"` on
the node that will be picked master . Log with level INFO to syslog::

    55 23 * * * /<path>/<to>/<virtualenv_name>/bin/clustercron -v -s elb <lb name> logger "clustercron run"


