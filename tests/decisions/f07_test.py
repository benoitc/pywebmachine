import t

class f07(t.Test):
    
    class TestResource(t.Resource):
        
        encodings = [
            ("identity", lambda x: x),
            ("reverse", lambda x: x[::-1])
        ]
        
        def encodings_provided(self, req, rsp):
            return self.encodings

        def reverse(self, data):
            return data[::-1]

        def to_html(self, req, rsp):
            return "foo"

    def test_no_encodings_provided(self):
        self.TestResource.encodings = None
        self.req.headers['accept-encoding'] = 'reverse'
        self.go()
        self.TestResource.encodings = [
            ('identity', lambda x: x),
            ('reverse', lambda x: x[::-1])
        ]
        
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_encoding, None)
        t.eq(self.rsp.body, 'foo')

    def test_no_acceptable_encoding(self):
        self.req.headers['accept-encoding'] = 'gzip'
        self.go()
        t.eq(self.rsp.status, '406 Not Acceptable')
        t.eq(self.rsp.body, '')

    def test_default(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'foo')
    
    def test_choose_reverse(self):
        self.req.headers['accept-encoding'] = 'reverse'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_encoding, 'reverse')
        t.eq(self.rsp.content_length, 3)
        t.eq(self.rsp.body, 'oof')

    def test_choose_idenity(self):
        self.req.headers['accept-encoding'] = 'identity, reverse;q=0.5'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_encoding, 'identity')
        t.eq(self.rsp.content_length, 3)
        t.eq(self.rsp.body, 'foo')

    # WebOb once again breaks content negotiation by not adding
    # identity with its implicit quality of 1.0
    # def test_implicit_identity(self):
    #     self.req.headers['accept-encoding'] = 'reverse;q=0.4'
    #     self.go()
    #     t.eq(self.rsp.status, '200 OK')
    #     t.eq(self.rsp.content_encoding, 'identity')
    #     t.eq(self.rsp.content_length, 3)
    #     t.eq(self.rsp.body, 'foo')