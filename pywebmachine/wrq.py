

class WebRequest(object):
    def method(self):
        pass
    
    def get_header(self, name):
        pass
    def get_header_list(self, name):
        pass
    
    def set_response_header(self, name, value):
        pass
    def get_response_header(self, name):
        pass
    def get_response_headers(self):
        pass
    
    def set_body(self, value):
        pass

    def set_meta(self, name, value):
        pass
    def get_meta(self, name):
        pass
    