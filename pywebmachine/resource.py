

class Resource(object):
    
    def __init__(self, req):
        self.req = req
    
    def ping(self, wrq):
        return (True, wrq)
    
    def service_available(self, wrq):
        return (True, wrq)
    
    def resource_exists(self, wrq):
        return (True, wrq)
    
    def auth_required(self, wrq):
        return (True, wrq)
    
    def is_authorized(self, wrq):
        return (True, wrq)
    
    def forbidden(self, wrq):
        return (False, wrq)
    
    def allow_missing_post(self, wrq):
        return (False, wrq)

    def uri_too_long(self, wrq):
        return (False, wrq)

    def malformed_request(self, wrq):
        return (False, wrq)
    
    def known_content_type(self, wrq):
        return (True, wrq)
    
    def valid_content_headers(self, wrq):
        return (True, wrq)
    
    def valid_entity_length(self, wrq):
        return (True, wrq)
    
    def options(self, wrq):
        return ([], wrq)
    
    def allowed_methods(self, wrq):
        return (["GET", "HEAD"], wrq)
    
    def known_methods(self, wrq):
        return ("GET HEAD POST PUT DELETE TRACE CONNECT OPTIONS".split(), wrq)

    def content_types_provided(self, wrq):
        return ([("text/html", lambda x: self.to_html(x))], wrq)
    
    def content_types_accepted(self, wrq):
        return ([], wrq)
    
    def delete_resource(self, wrq):
        return (False, wrq)
    
    def delete_completed(self, wrq):
        return (True, wrq)
    
    def post_is_create(self, wrq):
        return (False, wrq)

    def create_path(self, wrq):
        return (None, wrq)
    
    def process_post(self, wrq):
        return (False, wrq)

    def languages_available(self, wrq):
        return ([], wrq)
    
    def charsets_provided(self, wrq):
        """\
        return [("iso-8859-1", lambda x: x)]
        """
        return ([], wrq)

    def encodings_provided(self, wrq):
        return ([("identity", lambda x: x)], wrq)
    
    def variances(self, wrq):
        return ([], wrq)
    
    def is_conflict(self, wrq):
        return (False, wrq)
    
    def multiple_choices(self, wrq):
        return (False, wrq)
    
    def previously_existed(self, wrq):
        return (False, wrq)

    def moved_permanently(self, wrq):
        return (False, wrq)
    
    def moved_temporarily(self, wrq):
        return (False, wrq)
    
    def last_modified(self, wrq):
        return (None, wrq)
    
    def expires(self, wrq):
        return (None, wrq)
    
    def generate_etag(self, wrq):
        return (None, wrq)
    
    def finish_request(self, wrq):
        return (True, wrq)
