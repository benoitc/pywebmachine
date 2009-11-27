
class PyWMError(Exception):
    pass

class InternalServerError(PyWMError):
    def __init__(self, mesg):
        self.mesg = mesg

class MalformedRequest(PyWMError):
    def __init__(self, mesg):
        self.mesg = mesg