import t

class b08(t.Test):
    
    class TestResource(t.Resource):
        
        def authorized(self, req, rsp):
            return req.headers.get('authorization') == 'yay'

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.req.headers['authorization'] = 'yay'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '401 Unauthorized')
        t.eq(self.rsp.body, '')