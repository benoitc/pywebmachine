import t

class b13(t.Test):
    
    class TestResource(t.Resource):
        
        available = True
        pong = True
        
        def ping(self, req, rsp):
            print self.pong
            return self.pong

        def service_available(self, req, rsp):
            print self.available
            return self.available

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.TestResource.available = True
        self.TestResource.pong = True
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'nom nom')

    def test_no_ping(self):
        self.TestResource.available = True
        self.TestResource.pong = False
        self.go()
        t.eq(self.rsp.status, '503 Service Unavailable')
        t.eq(self.rsp.body, '')
    
    def test_no_service(self):
        self.TestResource.available = False
        self.TestResource.pong = True
        self.go()
        t.eq(self.rsp.status, '503 Service Unavailable')
        t.eq(self.rsp.body, '')