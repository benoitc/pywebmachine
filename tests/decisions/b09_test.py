import t

class b09(t.Test):
    
    class TestResource(t.Resource):
        
        def malformed_request(self, req, rsp):
            try:
                int(req.GET.get("value"))
                return False
            except:
                return True

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.req.query_string = 'value=1&foo=true'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req.query_string = 'value=false'
        self.go()
        t.eq(self.rsp.status, '400 Bad Request')
        t.eq(self.rsp.body, '')