import t

class p03(t.Test):
    
    class TestResource(t.Resource):

        conflict = False
        accepted = [('text/html', lambda r, s: s.write("bar") or True)]
        
        
        def allowed_methods(self, req, rsp):
            return ['PUT']
        
        def content_types_accepted(self, req, rsp):
            return self.accepted
        
        def is_conflict(self, req, rsp):
            return self.conflict
        
        def moved_permanently(self, req, rsp):
            return False

        def resource_exists(self, req, rsp):
            return False

        def to_html(self, req, rsp):
            return 'foo'

    def test_ok(self):
        self.TestResource.conflict = False
        self.req.method = 'PUT'
        self.req.content_type = 'text/html'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'bar')
    
    def test_conflict(self):
        self.TestResource.conflict = True
        self.req.method = 'PUT'
        self.go()
        t.eq(self.rsp.status, '409 Conflict')
        t.eq(self.rsp.body, '')
    
    def test_unsupported_media_type(self):
        prev = self.TestResource.accepted
        self.TestResource.accepted = []
        self.TestResource.conflict = False
        self.req.method = 'PUT'
        self.go()
        self.TestResource.accepted = prev
        t.eq(self.rsp.status, '415 Unsupported Media Type')
        t.eq(self.rsp.body, '')
    
