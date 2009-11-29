import t

class c04(t.Test):
    
    class TestResource(t.Resource):
        
        def content_types_provided(self, req, rsp):
            return [
                ('application/json', self.to_json),
                ('text/xml', self.to_xml)
            ]

        def to_json(self, req, rsp):
            return '{"nom": "nom"}'

        def to_xml(self, req, rsp):
            return "<nom>nom</nom>"

    def test_no_accept(self):
        # No Accept header means default to first specified.
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_type, 'application/json')
        t.eq(self.rsp.body, '{"nom": "nom"}')

    def test_none_acceptable(self):
        self.req.headers['accept'] = 'image/jpeg'
        self.go()
        t.eq(self.rsp.status, '406 Not Acceptable')
        t.eq(self.rsp.body, '')

    def test_json(self):
        self.req.headers['accept'] = 'application/json'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_type, 'application/json')
        t.eq(self.rsp.body, '{"nom": "nom"}')

    def test_xml(self):
        self.req.headers['accept'] = 'text/xml'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_type, 'text/xml')
        t.eq(self.rsp.body, '<nom>nom</nom>')
    
    def test_choose_best(self):
        self.req.headers['accept'] = 'text/xml;q=0.5, application/json;q=0.9'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_type, 'application/json')
        t.eq(self.rsp.body, '{"nom": "nom"}')