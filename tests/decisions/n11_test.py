import t

class n11(t.Test):
    
    class TestResource(t.Resource):
        
        create = False
        status = True
        location = '/foo'
        
        def allowed_methods(self, req, rsp):
            return ["POST"]
        
        def allow_missing_post(self, req, rsp):
            return True
        
        def content_types_accepted(self, req, rsp):
            return [('application/octet-stream', self.from_octets)]
        
        def created_location(self, req, rsp):
            return self.location
        
        def post_is_create(self, req, rsp):
            return self.create
        
        def process_post(self, req, rsp):
            if not self.create:
                rsp.body = "processed"
            return self.status
        
        def resource_exists(self, req, rsp):
            return False
        
        def from_octets(self, req, rsp):
            rsp.body = "created"
        
        def to_html(self, req, rsp):
            return "Yay"

    def test_post_is_create_no_redirect(self):
        self.TestResource.create = True
        self.TestResource.location = None
        self.req.method = 'POST'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'created')

    def test_post_is_create_redirect(self):
        self.TestResource.create = True
        self.TestResource.location = '/foo'
        self.req.method = 'POST'
        self.go()
        t.eq(self.rsp.status, '303 See Other')
        t.eq(self.rsp.location, '/foo')
        t.eq(self.rsp.body, 'created')

    def test_post_is_process(self):
        self.TestResource.create = False
        self.req.method = 'POST'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.location, None)
        t.eq(self.rsp.body, 'processed')
    
    def test_post_is_process_error(self):
        self.TestResource.create = False
        self.TestResource.status = False
        self.req.method = 'POST'
        self.go()
        self.TestResource.status = True
        t.eq(self.rsp.status, '500 Internal Server Error')
        t.eq(self.rsp.location, None)
        t.eq(self.rsp.body, '')