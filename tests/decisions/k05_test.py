import t

class k05(t.Test):
    
    class TestResource(t.Resource):

        moved = False
        
        def moved_permanently(self, req, rsp):
            return self.moved

        def previously_existed(self, req, rsp):
            return True

        def resource_exists(self, req, rsp):
            return False
        
        def to_html(self):
            return "Yay"

    def test_not_moved(self):
        self.TestResource.moved = False
        self.go()
        t.eq(self.rsp.status, '410 Gone')
        t.eq(self.rsp.body, '')
    
    def test_moved(self):
        self.TestResource.moved = '/foo'
        self.go()
        t.eq(self.rsp.status, '301 Moved Permanently')
        t.eq(self.rsp.location, '/foo')
        t.eq(self.rsp.body, '')
