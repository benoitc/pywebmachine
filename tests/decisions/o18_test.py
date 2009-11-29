import t

class o14(t.Test):
    
    class TestResource(t.Resource):
        
        multiple = True
        
        def allowed_methods(self, req, rsp):
            return ['GET', 'TRACE']
        
        def multiple_choices(self, req, rsp):
            return self.multiple

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_ok(self):
        self.TestResource.multiple = False
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'foo')
    
    def test_multiple(self):
        self.TestResource.multiple = True
        self.go()
        t.eq(self.rsp.status, '300 Multiple Choices')
        t.eq(self.rsp.body, 'foo')

    def test_multiple_no_body(self):
        self.TestResource.multiple = True
        self.req.method = 'TRACE'
        self.go()
        t.eq(self.rsp.status, '300 Multiple Choices')
        t.eq(self.rsp.body, '')