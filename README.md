# Clustercron


![image](https://img.shields.io/pypi/v/clustercron.svg%0A%20%20%20%20%20:target:%20https://pypi.python.org/pypi/clustercron)

![image](https://img.shields.io/travis/maartenq/clustercron.svg%0A%20%20%20%20%20:target:%20https://travis-ci.org/maartenq/clustercron)

![image](https://readthedocs.org/projects/clustercron/badge/?version=latest%0A%20%20%20%20%20:target:%20https://clustercron.readthedocs.io/en/latest/?badge=latest%0A%20%20%20%20%20:alt:%20Documentation%20Status)

![image](https://codecov.io/github/maartenq/clustercron/coverage.svg?branch=master%0A%20%20%20%20%20:target:%20https://codecov.io/github/maartenq/clustercron?branch=master)

**Clustercron** is cronjob wrapper that tries to ensure that a script gets run
only once, on one host from a pool of nodes of a specified loadbalancer.
**Clustercron** select a *master* from all nodes and will run the cronjob only
on that node.

*   Free software: ISC license
*   Documentation: <https://clustercron.readthedocs.org/en/latest/>

## Features

Supported load balancers (till now):

* AWS Elastic Load Balancing (ELB)
* AWS Elastic Load Balancing v2 (ALB)
