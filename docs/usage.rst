Usage
=====

clustercron help::

    $ clustercron --help
    usage:
       clustercron [(-v|--verbose)] elb <loadbalancer_name> [<cron_command>]
       clustercron --version
       clustercron (-h|--help)

    Clustercron is cronjob wrapper that tries to ensure that a script gets run
    only once, on one host from a pool of nodes of a specified loadbalancer.

    Without specifying a <cron_command> clustercron will only check if the node
    is the `master` in the cluster and will return 0 if so and return 2 if not.
