# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import os
import time


_version = "0.1.%sdev" % int(time.time())
_packages = find_packages('womble', exclude=["*.tests", "*.tests.*", "tests.*", "tests"])


def _strip_comments(line):
    return line.split('#', 1)[0].strip()

with open( os.path.join( os.path.dirname(__file__), 'requirements.txt' ) ) as f:
    _install_requires = f.readlines()
    _install_requires = map(_strip_comments, _install_requires)
    _install_requires = filter( lambda x:x.strip()!='', _install_requires )


package_info = {
    'name'             : 'ticket_womble',
    'version'          : _version,
    'packages'         : _packages,
    'install_requires' : _install_requires,
    'scripts'          : ( 'scripts/sync_tickets', ),
}

setup(**package_info)
