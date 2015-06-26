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

    Clustercron is cronjob wrapper that tries to ensure that a script gets run
    only once, on one host from a pool of nodes of a specified loadbalancer.

    Without specifying a <cron_command> clustercron will only check if the node
    is the `master` in the cluster and will return 0 if so.


Command line
------------

Clustercron can be run from command line for debugging.

Check if node is master::

    $ clustercron elb ldmd
    $ echo $?
    1


Check if node is master with verbose (info) output::

    $ clustercron -v elb ldmd
    INFO     clustercron.elb : Instance ID: i-ca289460
    INFO     clustercron.elb : All instances: i-58e224a1, i-ca289460 Instance in list: True
    INFO     clustercron.elb : Instances in service: i-58e224a1, i-ca289460 Instance in list: True
    INFO     clustercron.elb : This instance master: False


Cron entry example
------------------

/etc/cron.d/cron_example::

    # For details see man 4 crontabs

    # Example of job definition:
    # .---------------- minute (0 - 59)
    # |  .------------- hour (0 - 23)
    # |  |  .---------- day of month (1 - 31)
    # |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
    # |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
    # |  |  |  |  |
    # *  *  *  *  * user-name command to be executed
    42 * * * * /<path>/<to>/clustercron/bin/clustercron -v -s elb <lb name> logger "clustercron run"


