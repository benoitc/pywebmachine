import t

class b04(t.Test):
    
    class TestResource(t.Resource):
        
        def valid_entity_length(self, req, rsp):
            return req.content_length < 1024

        def to_html(self, req, rsp):
            return "yay good"
    
    def test_ok(self):
        self.req.body = 'foo'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'yay good')

    def test_not_ok(self):
        self.req.body = 'foo' * 1024
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '413 Request Entity Too Large')
        t.eq(self.rsp.body, '')