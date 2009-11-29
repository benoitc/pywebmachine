import t

class o14(t.Test):
    
    class TestResource(t.Resource):
        
        conflict = True
        
        def allowed_methods(self, req, rsp):
            return ["PUT"]

        def is_conflict(self, req, rsp):
            return self.conflict

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_ok(self):
        self.TestResource.conflict = False
        self.req.method = 'PUT'
        self.go()
        t.eq(self.rsp.status, '204 No Content')
        t.eq(self.rsp.body, '')
    
    def test_conflict(self):
        self.TestResource.conflict = True
        self.req.method = 'PUT'
        self.go()
        t.eq(self.rsp.status, '409 Conflict')
        t.eq(self.rsp.body, '')
