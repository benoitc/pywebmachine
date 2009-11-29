import t

class b10(t.Test):
    
    class TestResource(t.Resource):
        
        def allowed_methods(self, req, rsp):
            return ["GET"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req.method = 'POST'
        self.go()
        t.eq(self.rsp.status, '405 Method Not Allowed')
        t.eq(self.rsp.body, '')