syncstats
=========

SyncStats is a service with REST interface to collect user statistics for synchrotron related projects.



Python requirements:

- Python 2.7+

Required Python packages:

- Tornado 2.4.1+ (http://www.tornadoweb.org/)
- Django 1.5.0+ (https://www.djangoproject.com/)


Installation
------------

On Centos 6.3 (as root):

1. Ensure pip is installed: easy_install pip
2. Ensure git, gcc and python dev are installed: yum install -y git gcc python-devel
3. Install the instance tools from GitHub: pip install git+https://github.com/AustralianSynchrotron/syncstats

On Ubuntu 12.10 (as user):

1. sudo apt-get update
2. sudo apt-get -y install python-pip
3. sudo apt-get -y install git
4. sudo pip install git+https://github.com/AustralianSynchrotron/syncstats