import t

class b07(t.Test):
    
    class TestResource(t.Resource):
        
        def forbidden(self, req, rsp):
            return req.cookies.get('id') != 'foo'

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.req.headers['cookie'] = 'id=foo'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req.headers['cookie'] = 'bar'
        self.go()
        t.eq(self.rsp.status, '403 Forbidden')
        t.eq(self.rsp.body, '')