import t

class b06(t.Test):
    
    class TestResource(t.Resource):
        
        def valid_content_headers(self, req, rsp):
            # Not sure what this is intended for.
            for h in req.headers:
                if not h.lower().startswith("content-"):
                    continue
                if h[8:].lower() not in ["type", "length"]:
                    return False
            return True

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.req.headers['content-type'] = 'text/plain'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_not_ok(self):
        self.req.headers['content-foo'] = 'bizbang'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '501 Not Implemented')
        t.eq(self.rsp.body, '')