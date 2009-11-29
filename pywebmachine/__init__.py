
from decisions import process
from resource import Resource

def execute(klass, req, rsp):
    try:
        return process(klass, req, rsp)
    except webob.exc.HTTPException, error:
        return error