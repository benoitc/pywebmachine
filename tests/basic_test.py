
import t

class Basics(t.Test):
    
    class TestResource(t.Resource):
        def to_html(self, req, rsp):
            return "Hello, world!"
    
    def test_basic(self):
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, "Hello, world!")

        