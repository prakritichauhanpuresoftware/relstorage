##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""A backend for ZODB that stores pickles in a relational database."""

VERSION = "1.7.0a1.dev0"

# The choices for the Trove Development Status line:
# Development Status :: 5 - Production/Stable
# Development Status :: 4 - Beta
# Development Status :: 3 - Alpha

classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
"""

import os
import platform
from setuptools import setup

py_impl = getattr(platform, 'python_implementation', lambda: None)
is_pypy = py_impl() == 'PyPy'
is_pure = os.environ.get('PURE_PYTHON')

doclines = __doc__.split("\n")


def read_file(*path):
    base_dir = os.path.dirname(__file__)
    file_path = (base_dir, ) + tuple(path)
    f = file(os.path.join(*file_path))
    result = f.read()
    f.close()
    return result

setup(
    name="RelStorage",
    version=VERSION,
    author="Zope Foundation and Contributors",
    maintainer="Shane Hathaway",
    maintainer_email="shane@hathawaymix.org",
    url="http://pypi.python.org/pypi/RelStorage",
    packages=[
        'relstorage',
        'relstorage.adapters',
        'relstorage.adapters.tests',
        'relstorage.tests',
        'relstorage.tests.blob',
    ],
    package_data={
        'relstorage': ['component.xml'],
    },
    license="ZPL 2.1",
    platforms=["any"],
    description=doclines[0],
    classifiers=filter(None, classifiers.split("\n")),
    long_description=(
        read_file("README.txt") + "\n\n" +
        "Change History\n" +
        "==============\n\n" +
        read_file("CHANGES.txt")),
    zip_safe=False,  # otherwise ZConfig can't see component.xml
    install_requires=[
        'perfmetrics',
        'ZODB >= 4.3.0, <5.0',
        # ZEO is needed for blob layout
        'ZEO >= 4.2.0b1, <5.0',
        'zope.interface',
        'zc.lockfile',
    ],
    tests_require=[
        'mock',
        'zope.testing',
    ],
    extras_require={
        # On PyPy, PyMySQL >= 0.7 raises a MemoryError (and 0.6.7 spuriously raises 'MySql gone away 2006)
        # see https://github.com/PyMySQL/PyMySQL/issues/474
        'mysql': ['MySQL-python>=1.2.2' if not is_pypy and not is_pure else 'PyMySQL==0.6.6'],
        'postgresql': ['psycopg2>=2.0' if not is_pypy and not is_pure else 'psycopg2cffi>=2.7.0'],
        'oracle': ['cx_Oracle>=4.3.1'],
    },
    entry_points = {
        'console_scripts': [
            'zodbconvert = relstorage.zodbconvert:main',
            'zodbpack = relstorage.zodbpack:main',
        ],
        'zodburi.resolvers': [
            ('postgres = '
             'relstorage.zodburi_resolver:postgresql_resolver [postgresql]'),
            'mysql = relstorage.zodburi_resolver:mysql_resolver [mysql]',
            'oracle = relstorage.zodburi_resolver:oracle_resolver [oracle]'
        ]},
    test_suite='relstorage.tests.alltests.make_suite',
)
