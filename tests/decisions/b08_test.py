import t

class b08(t.Test):
    
    class TestResource(t.Resource):
        
        def is_authorized(self, req, rsp):
            if req.headers.get('authorization') == 'yay':
                return True
            return 'oauth'

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.req.headers['authorization'] = 'yay'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.go()
        t.eq(self.rsp.status, '401 Unauthorized')
        t.eq(self.rsp.headers['www-authenticate'], 'oauth')
        t.eq(self.rsp.body, '')