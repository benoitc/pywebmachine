# Copyright 2009 Paul J. Davis <paul.joseph.davis@gmail.com>
#
# This file is part of the pywebmachine package released
# under the MIT license.
import unittest
import webob
import webob.exc

from pywebmachine import process, Resource

class Test(unittest.TestCase):
    def setUp(self):
        self.req = webob.Request.blank("/")
        self.rsp = webob.Response()

    def go(self):
        try:
            process(self.TestResource, self.req, self.rsp)
        except webob.exc.HTTPException, error:
            self.rsp = error

def eq(a, b):
    assert a == b, "%r != %r" % (a, b)

def ne(a, b):
    assert a != b, "%r == %r" % (a, b)

def lt(a, b):
    assert a < b, "%r >= %r" % (a, b)

def gt(a, b):
    assert a > b, "%r <= %r" % (a, b)

def isin(a, b):
    assert a in b, "%r is not in %r" % (a, b)

def isnotin(a, b):
    assert a not in b, "%r is in %r" % (a, b)

def has(a, b):
    assert hasattr(a, b), "%r has no attribute %r" % (a, b)

def hasnot(a, b):
    assert not hasattr(a, b), "%r has an attribute %r" % (a, b)

def raises(exctype, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exctype, inst:
        pass
    else:
        func_name = getattr(func, "func_name", "<builtin_function>")
        raise AssertionError("Function %s did not raise %s" % (
            func_name, exctype.__name__))

