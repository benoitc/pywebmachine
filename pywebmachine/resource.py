

class Resource(object):
    
    def __init__(self, wrq):
        self.wrq = wrq
    
    def ping(self):
        return True
    
    def service_available(self):
        return True
    
    def resource_exists(self):
        return True
    
    def auth_required(self):
        return True
    
    def is_authorized(self):
        return True
    
    def forbidden(self):
        return False
    
    def allow_missing_post(self):
        return False

    def uri_too_long(self):
        return False

    def malformed_request(self):
        return False
    
    def known_content_type(self):
        return True
    
    def valid_content_headers(self):
        return True
    
    def valid_entity_length(self):
        return True
    
    def options(self):
        return []
    
    def allowed_methods(self):
        return ["GET", "HEAD"]
    
    def known_methods(self):
        return [
            "GET", "HEAD", "POST", "PUT", "DELETE",
            "TRACE", "CONNECT", "OPTIONS"
        ]

    def content_types_provided(self):
        return [
            ("text/html", lambda x: self.to_html(x))
        ]
    
    def content_types_accepted(self):
        return None
    
    def delete_resource(self):
        return False
    
    def delete_completed(self):
        return True
    
    def post_is_create(self):
        return False

    def create_path(self):
        return None
    
    def process_post(self):
        return False

    def languages_available(self):
        return None
    
    def charsets_provided(self):
        """\
        return [("iso-8859-1", lambda x: x)]
        """
        return None

    def encodings_provided(self):
        return [
            ("identity", lambda x: x)
        ]
    
    def variances(self):
        return []
    
    def is_conflict(self):
        return False
    
    def multiple_choices(self):
        return False
    
    def previously_existed(self):
        return False

    def moved_permanently(self):
        return False
    
    def moved_temporarily(self):
        return False
    
    def last_modified(self):
        return None
    
    def expires(self):
        return None
    
    def generate_etag(self):
        return None
    
    def finish_request(self):
        return True
