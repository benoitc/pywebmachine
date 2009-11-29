import t

class e06(t.Test):
    
    class TestResource(t.Resource):
        charsets = ["UTF-8", "iso-8859-1"]
        
        def charsets_provided(self, req, rsp):
            return self.charsets

        def to_html(self, req, rsp):
            if rsp.charset == 'UTF-8':
                return "unicode!"
            else:
                return "ascii!"
    
    def test_no_charsets(self):
        self.TestResource.charsets = None
        self.req.headers['accept-charset'] = 'iso-8859-1'
        self.go()
        self.TestResource.charsets = ['utf-8', 'iso-8859-1']
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.charset, None)
        t.eq(self.rsp.body, 'ascii!')
    
    def test_none_acceptable(self):
        self.TestResource.charsets = ['utf-8']
        self.req.headers['accept-charset'] = 'latin-1'
        self.go()
        self.TestResource.charsets = ['utf-8', 'iso-8859-1']
        print self.rsp.charset
        t.eq(self.rsp.status, '406 Not Acceptable')
        t.eq(self.rsp.body, '')
    
    def test_default(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.charset, None)
        t.eq(self.rsp.body, 'ascii!')

    def test_choose_utf_8(self):
        self.req.headers['accept-charset'] = 'utf-8'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.charset, 'UTF-8')
        t.eq(self.rsp.body, 'unicode!')

    def test_choose_iso_8859_1(self):
        self.req.headers['accept-charset'] = 'iso-8859-1;q=0.8, utf-8;q=0.2'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.charset, 'iso-8859-1')
        t.eq(self.rsp.body, 'ascii!')

    # WebOb's charset chooser doesn't provide the implicity
    # quality of 1.0 for iso-8859-1 when it's not mentioned
    # def test_implicit_iso_8859_1(self):
    #     self.req.headers['accept-charset'] = 'utf-8;q=0.2'
    #     self.go()
    #     t.eq(self.rsp.status, '200 OK')
    #     t.eq(self.rsp.charset, 'iso-8859-1')
    #     t.eq(self.rsp.body, 'ascii!')
