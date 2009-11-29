#! /usr/bin/env python

import optparse as op
from wsgiref.simple_server import make_server

import pywebmachine as pwm
import routes
import webob
import webob.exc

class MyResource(pwm.Resource):
    def to_html(self, req, rsp):
        return "<html><body>Stuff!</body></html>"

map = routes.Mapper()
map.connect("/", resource=MyResource)

def application(environ, start_response):
    req = webob.Request(environ)
    rsp = webob.Response()

    match = map.routematch(req.path)
    if match is None:
        rsp = webob.exc.HTTPNotFound()
    else:
        res = match[0]["resource"]
        try:
            pwm.process(res, req, rsp)
        except webob.exc.HTTPException, error:
            rsp = error

    return rsp(environ, start_response)

def options():
    return [
        op.make_option('-a', dest='address', default='127.0.0.1',
            help = 'Address to listen on. [%default]'),
        op.make_option('-p', dest='port', default=8080, type='int',
            help = 'Port to listen on. [%default]')
    ]

def main():
    parser = op.OptionParser(usage='%prog [OPTIONS]', option_list=options())
    opts, args = parser.parse_args()
    if len(args):
        parser.error("Unknown arguments: %r" % args)

    server = make_server(opts.address, opts.port, application)
    server.serve_forever()

if __name__ == '__main__':
    main()
