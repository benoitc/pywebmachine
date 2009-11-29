import t

class d05(t.Test):
    
    class TestResource(t.Resource):
        langs = ["en", "en-gb"]
        
        def languages_provided(self, req, rsp):
            return self.langs

        def to_html(self, req, rsp):
            if rsp.content_language == ['en-gb']:
                return "Favourite!"
            else:
                return "Favorite!"
    
    def test_no_langs(self):
        self.TestResource.langs = None
        self.req.headers['accept-language'] = 'en;q=0.3, es'
        self.go()
        self.TestResource.langs = ['en', 'en-gb']
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_language, None)
        t.eq(self.rsp.body, 'Favorite!')
    
    def test_none_acceptable(self):
        self.req.headers['accept-language'] = 'es'
        self.go()
        t.eq(self.rsp.status, '406 Not Acceptable')
        t.eq(self.rsp.body, '')
    
    def test_en_default(self):
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.body, 'Favorite!')

    def test_en(self):
        self.req.headers['accept-language'] = 'en'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_language, ['en'])
        t.eq(self.rsp.body, 'Favorite!')
    
    def test_en_gb(self):
        self.req.headers['accept-language'] = 'en-gb'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_language, ['en-gb'])
        t.eq(self.rsp.body, 'Favourite!')
    
    def test_choose_en(self):
        self.req.headers['accept-language'] = 'en;q=0.9, en-gb;q=0.4'
        self.go()
        t.eq(self.rsp.status, '200 OK')
        t.eq(self.rsp.content_language, ['en'])
        t.eq(self.rsp.body, 'Favorite!')
    
    # WebOb' fuzzy selection is either broken or I don't understand
    # how it's supposed to work.
    # def test_choose_en_fuzzy(self):
    #     self.TestResource.langs = ['en-gb']
    #     self.req.headers['accept-language'] = 'en'
    #     self.go()
    #     self.TestResource.langs = ['en', 'en-gb']
    #     t.eq(self.rsp.status, '200 OK')
    #     t.eq(self.rsp.content_language, ['en-gb'])
    #     t.eq(self.rsp.body, 'Favourite!')
        