import t

class g11(t.Test):
    
    class TestResource(t.Resource):
        
        done = True
        
        def allowed_methods(self, req, rsp):
            return ["DELETE"]

        def delete_completed(self, req, rsp):
            return self.done

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_done(self):
        self.TestResource.done = True
        self.req.method = 'DELETE'
        self.go()
        t.eq(self.rsp.status, '204 No Content')
        t.eq(self.rsp.body, '')
    
    def test_not_done(self):
        self.TestResource.done = False
        self.req.method = 'DELETE'
        self.go()
        t.eq(self.rsp.status, '202 Accepted')
        t.eq(self.rsp.body, '')
