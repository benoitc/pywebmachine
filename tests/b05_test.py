import t

class b05(t.Test):
    
    class TestResource(t.Resource):
        
        def known_content_type(self, req, rsp):
            return req.content_type.split(';')[0] in ["text/plain", "text/xml"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.req.headers['content-type'] = 'text/plain'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req.headers['content-type'] = 'application/json; charset=utf-8'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '415 Unsupported Media Type')
        t.eq(self.rsp.body, '')