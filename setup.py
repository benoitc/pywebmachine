# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.


import os
from setuptools import setup, find_packages

from pywebmachine import __version__

setup(
    name = 'pywebmachine',
    version = __version__,

    description = 'WSGI REST Toolkit',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),

    author = 'Paul J. Davis',
    author_email = 'paul.joseph.davis@gmail.com',
    license = 'MIT',
    url = 'http://github.com/davisp/pywebmachine',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe = True,
    packages = find_packages(exclude=['examples', 'tests']),
    include_package_data = True,

    install_requires = [
        'webob',
        'routes'
    ],

    test_suite = 'nose.collector',
)
