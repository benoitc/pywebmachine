import t

class m05(t.Test):
    
    class TestResource(t.Resource):
        
        allow = True
        
        def allowed_methods(self, req, rsp):
            return ["POST"]
        
        def allow_missing_post(self, req, rsp):
            return self.allow
        
        def process_post(self, req, rsp):
            rsp.body = "processed"
            return True
        
        def resource_exists(self, req, rsp):
            return False
        
        def to_html(self):
            return "Yay"

    def test_allow_post(self):
        self.TestResource.allow = True
        self.req.method = 'POST'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'processed')
    
    def test_dont_allow(self):
        self.TestResource.allow = False
        self.req.method = 'POST'
        self.go()
        t.eq(self.rsp.status, '404 Not Found')
        t.eq(self.rsp.body, '')