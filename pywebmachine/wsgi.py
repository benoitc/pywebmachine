# -*- coding: utf-8 -*-
#
# This file is part of pywebmachine released under the MIT license.
# See the NOTICE for more information.
import routes
import webob
import webob.exc

from .decisions import process

class WSGIMachine(object):

    def __init__(self, paths):
        self.route_map = routes.Mapper()
        for path, res in paths:
            self.route_map.connect(path, resource=res)

    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        rsp = webob.Response()

        match = self.route_map.routematch(req.path)
        if match is None:
            rsp = webob.exc.HTTPNotFound()
        else:
            res = match[0]["resource"]
            try:
                process(res, req, rsp)
            except webob.exc.HTTPException, error:
                rsp = error

        return rsp(environ, start_response)
