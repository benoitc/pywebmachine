import t

class g07(t.Test):
    
    class TestResource(t.Resource):

        exists = True

        def charsets_provided(self, req, rsp):
            return ['utf-8', 'iso-8859-1']

        def content_types_provided(self, req, rsp):
            return [
                ('text/html', self.to_html),
                ('text/plain', self.to_plain)
            ]

        def encodings_provided(self, req, rsp):
            return [
                ('identity', lambda x: x),
                ('gzip', lambda x: x)
            ]
        
        def languages_provided(self, req, rsp):
            return ['en', 'en-gb', 'es']
        
        def resource_exists(self, req, rsp):
            return self.exists
        
        def variances(self, req, rsp):
            return ["Cookie"]

        def to_html(self, req, rsp):
            return "<html><body>foo</body></html>"
        
        def to_plain(self, req, rsp):
            return "foo"

    def test_variances(self):
        self.TestResource.exists = True
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(sorted(self.rsp.vary), [
            'Accept', 'Accept-Charset', 'Accept-Encoding',
            'Accept-Language', 'Cookie'
        ])

    def test_resource_not_exists(self):
        self.TestResource.exists = False
        self.go()
        t.eq(self.rsp.status, '404 Not Found')
        t.eq(self.rsp.body, '')
        