
class PyWMError(Exception):
    pass

class Halt(PyWMError):
    def __init__(self, code):
        self.code = code

class InternalServerError(PyWMError):
    def __init__(self, mesg):
        self.code = 500
        self.mesg = mesg

class MalformedRequest(PyWMError):
    def __init__(self, mesg):
        self.code = 400
        self.mesg = mesg