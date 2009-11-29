import t

class k07(t.Test):
    
    class TestResource(t.Resource):

        existed = False
        
        def previously_existed(self, req, rsp):
            return self.existed

        def resource_exists(self, req, rsp):
            return False
        
        def to_html(self):
            return "Yay"

    def test_not_existed(self):
        self.TestResource.existed = False
        self.go()
        t.eq(self.rsp.status, '404 Not Found')
        t.eq(self.rsp.body, '')
    
    def test_existed(self):
        self.TestResource.existed = True
        self.go()
        t.eq(self.rsp.status, '410 Gone')
        t.eq(self.rsp.body, '')