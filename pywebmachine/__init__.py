# -*- coding: utf-8 -*-
#
# This file is part of pywebmachine released under the MIT license.
# See the NOTICE for more information.

version_info = (0, 1, 0)
__version__ = ".".join(map(str, version_info))

try:
    from pywebmachine.decisions import process
    from pywebmachine.resource import Resource
    from pywebmachine.wsgi import WSGIMachine

except ImportError:
    import traceback
    traceback.print_exc()
