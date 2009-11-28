
import t

class b03(t.Test):
    
    class TestResource(t.Resource):
        def allowed_methods(self, req, rsp):
            return ["GET", "OPTIONS"]

        def options(self, req, rsp):
            return [("X-Noah", "Awesome")]

        def to_html(self, req, rsp):
            return "Hello, world!"
    
    def test_get(self):
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.headers.get('X-Noah'), None)
        t.eq(self.rsp.body, 'Hello, world!')

    def test_options(self):
        self.req.method = 'OPTIONS'
        t.process(self.TestResource, self.req, self.rsp)
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.headers['X-Noah'], 'Awesome')
        t.eq(self.rsp.body, '')