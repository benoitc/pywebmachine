import t

class g11(t.Test):
    
    class TestResource(t.Resource):
        
        def generate_etag(self, req, rsp):
            return "bar"

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_no_if_match(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.etag, 'bar')
        t.eq(self.rsp.body, 'foo')
    
    def test_if_match_ok(self):
        self.req.headers['if-match'] = 'bar'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.etag, 'bar')
        t.eq(self.rsp.body, 'foo')
    
    def test_if_match_fail(self):
        self.req.headers['if-match'] = 'baz'
        self.go()
        t.eq(self.rsp.status, '412 Precondition Failed')
        t.eq(self.rsp.body, '')