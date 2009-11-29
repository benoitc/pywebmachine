import t

class b11(t.Test):
    
    class TestResource(t.Resource):
        
        def uri_too_long(self, req, rsp):
            return len(req.url) > 100

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req = t.webob.Request.blank('/foo' * 40)
        self.go()
        t.eq(self.rsp.status, '414 Request URI Too Long')
        t.eq(self.rsp.body, '')