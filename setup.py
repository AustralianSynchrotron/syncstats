from __future__ import with_statement
from distutils.core import setup



exec(open('core/version.py').read())

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='SyncStats',
    version=__version__,
    description='Service with REST interface to collect user statistics for synchrotron related projects',
    long_description=long_description,
    url='https://github.com/AustralianSynchrotron/syncstats',
    author='Andreas Moll',
    author_email='andreas.moll@synchrotron.org.au',
    packages=['syncstats', 'syncstats/core', 'syncstats/pluginmanager', 'syncstats/stats', 'syncstats/webapp', 'syncstats/example'],
    install_requires=[
        'django>=1.5',
        'argparse',
        'tornado >= 2.4.1',
        'pyinotify >= 0.9.4',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Modified BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    license='Modified BSD',
    scripts=['syncstatsd'],
)
