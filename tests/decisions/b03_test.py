
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
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.headers.get('X-Noah'), None)
        t.eq(self.rsp.body, 'Hello, world!')

    def test_options(self):
        self.req.method = 'OPTIONS'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.headers['X-Noah'], 'Awesome')
        t.eq(self.rsp.body, '')
    
    # Fairly unrelated, but no good place to put this
    def test_non_unicode_body(self):
        prev = self.TestResource.to_html
        def my_html(self, req, rsp):
            rsp.charset = None
            return "Hi"
        self.TestResource.to_html = my_html
        self.go()
        self.TestResource.to_html = prev
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'Hi')
        