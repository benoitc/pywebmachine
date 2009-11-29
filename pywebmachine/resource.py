
class Resource(object):

    def __init__(self, req, rsp):
        pass

    def allowed_methods(self, req, rsp):
        return ["GET", "HEAD"]

    def allow_missing_post(self, req, rsp):
        return False

    def auth_required(self, req, rsp):
        return True
    
    def charsets_provided(self, req, rsp):
        """\
        return [("iso-8859-1", lambda x: x)]
        
        Returning None prevents the character set negotiation
        logic.
        """
        return None

    def content_types_accepted(self, req, rsp):
        return None

    def content_types_provided(self, req, rsp):
        return [
            ("text/html", self.to_html)
        ]

    def created_location(self, req, rsp):
        return None

    def delete_completed(self, req, rsp):
        return True
    
    def delete_resource(self, req, rsp):
        return False

    def encodings_provided(self, req, rsp):
        return [
            ("identity", lambda x: x)
        ]

    def expires(self, req, rsp):
        return None
    
    def finish_request(self, req, rsp):
        return True

    def forbidden(self, req, rsp):
        return False
    
    def generate_etag(self, req, rsp):
        return None

    def is_authorized(self, req, rsp):
        return True
    
    def is_conflict(self, req, rsp):
        return False

    def known_content_type(self, req, rsp):
        return True

    def known_methods(self, req, rsp):
        return set([
            "GET", "HEAD", "POST", "PUT", "DELETE",
            "TRACE", "CONNECT", "OPTIONS"
        ])

    def languages_provided(self, req, rsp):
        """\
        return ["en", "es", "en-gb"]
        
        returning None short circuits the language negotiation.
        """
        return None

    def last_modified(self, req, rsp):
        return None

    def malformed_request(self, req, rsp):
        return False

    def moved_permanently(self, req, rsp):
        return False
    
    def moved_temporarily(self, req, rsp):
        return False
    
    def multiple_choices(self, req, rsp):
        return False

    def options(self, req, rsp):
        return []

    def ping(self, req, rsp):
        return True
    
    def post_is_create(self, req, rsp):
        return False
    
    def previously_existed(self, req, rsp):
        return False

    def process_post(self, req, rsp):
        return False

    def resource_exists(self, req, rsp):
        return True
    
    def service_available(self, req, rsp):
        return True

    def uri_too_long(self, req, rsp):
        return False
    
    def valid_content_headers(self, req, rsp):
        return True
    
    def valid_entity_length(self, req, rsp):
        return True

    def variances(self, req, rsp):
        return []
