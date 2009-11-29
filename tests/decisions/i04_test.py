import t

class i04(t.Test):
    
    class TestResource(t.Resource):

        moved = False
        
        def allowed_methods(self, req, rsp):
            return ['PUT']
        
        def content_types_accepted(self, req, rsp):
            return [('text/html', self.from_html)]
        
        def moved_permanently(self, req, rsp):
            return self.moved

        def resource_exists(self, req, rsp):
            return False

        def from_html(self, req, rsp):
            rsp.body = 'bar'

        def to_html(self, req, rsp):
            return 'foo'

    def test_not_moved(self):
        self.TestResource.moved = False
        self.req.method = 'PUT'
        self.req.content_type = 'text/html'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'bar')
    
    def test_moved(self):
        self.TestResource.moved = '/foo'
        self.req.method = 'PUT'
        self.go()
        t.eq(self.rsp.status, '301 Moved Permanently')
        t.eq(self.rsp.location, '/foo')
