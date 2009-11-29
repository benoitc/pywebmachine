import t

class b12(t.Test):
    
    class TestResource(t.Resource):
        
        def known_methods(self, req, rsp):
            return ["GET"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req.method = 'PUT'
        self.go()
        t.eq(self.rsp.status, '501 Not Implemented')
        t.eq(self.rsp.body, '')