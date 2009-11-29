import t

class k13(t.Test):
    
    class TestResource(t.Resource):

        def generate_etag(self, req, rsp):
            return 'foo'

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return 'bar'

    def test_etag_match(self):
        self.req.headers['if-none-match'] = 'foo'
        self.go()
        t.eq(self.rsp.status, '304 Not Modified')
        t.eq(self.rsp.etag, 'foo')
        t.eq(self.rsp.body, '')
    
    def test_modified(self):
        self.req.headers['if-none-match'] = 'bar'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.etag, 'foo')
        t.eq(self.rsp.body, 'bar')
