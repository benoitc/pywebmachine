
import datetime
import types

import webob.exc

def b03(res, req, rsp):
    "Options?"
    if req.method == 'OPTIONS':
        for (header, value) in res.options(req, rsp):
            rsp.headers[header] = value
        return True
    return False

def b04(res, req, rsp):
    "Request entity too large?"
    return not res.valid_entity_length(req, rsp)

def b05(res, req, rsp):
    "Unknown Content-Type?"
    return not res.known_content_type(req, rsp)

def b06(res, req, rsp):
    "Unknown or unsupported Content-* header?"
    return not res.valid_content_headers(req, rsp)

def b07(res, req, rsp):
    "Forbidden?"
    return res.forbidden(req, rsp)

def b08(res, req, rsp):
    "Authorized?"
    resp = res.is_authorized(req, rsp)
    if resp is True:
        return True
    elif isinstance(resp, basestring):
        rsp.headers["WWW-Authenticate"] = resp
    return False

def b09(res, req, rsp):
    "Malformed?"
    return res.malformed_request(req, rsp)

def b10(res, req, rsp):
    "Is method allowed?"
    if req.method in res.allowed_methods(req, rsp):
        return True
    rsp.allowed = res.allowed_methods(req, rsp)
    return False

def b11(res, req, rsp):
    "URI too long?"
    return res.uri_too_long(req, rsp)

def b12(res, req, rsp):
    "Known method?"
    return req.method in res.known_methods(req, rsp)

def b13(res, req, rsp):
    "Service available?"
    return res.ping(req, rsp) and res.service_available(req, rsp)

def c03(res, req, rsp):
    "Accept exists?"
    return "accept" in req.headers

def c04(res, req, rsp):
    "Acceptable media type available?"
    ctypes = [ctype for (ctype, func) in req.content_types_accepted(req, rsp)]
    ctype = req.accept.best_match(ctypes)
    if ctype is None:
        return False
    rsp.content_type = ctype
    return True

def d04(res, req, rsp):
    "Accept-Language exists?"
    return "accept-language" in req.headers

def d05(res, req, rsp):
    "Accept-Language available?"
    langs = res.languages_available(req, rsp)
    lang = req.accept_language.best_match(langs)
    if lang is None:
        return False
    rsp.content_language = lang
    return True
    
def e05(res, req, rsp):
    "Accept-Charset exists?"
    return "accept-charset" in req.headers

def e06(res, req, rsp):
    "Acceptable charset available?"
    charsets = res.charsets_provided(req, rsp)
    if not charsets:
        return True
    charsets = [cs for (cs, func) in charsets]
    charset = req.accept_charset.best_match(charsets)
    if charset is None:
        return False
    rsp.charset = charset
    return True

def f06(res, req, rsp):
    "Accept-Encoding exists?"
    return "accept-encoding" in req.headers

def f07(res, req, rsp):
    "Acceptable encoding available?"
    encodings = [enc for (enc, func) in res.charsets_provided(req, rsp)]
    enc = req.accept_encoding.best_match(encodings)
    if enc is None:
        return False
    rsp.content_encoding = enc
    return True

def g07(res, req, rsp):
    "Resource exists?"

    # Set variances now that conneg is done
    hdr = []
    if len(res.content_types_provided(req, rsp) or []) > 1:
        hdr.append("Accept")
    if len(res.charsets_provided(req, rsp) or []) > 1:
        hdr.append("Accept-Charset")
    if len(res.encodings_provided(req, rsp) or []) > 1:
        hdr.append("Accept-Encoding")
    if len(res.languages_provided(req, rsp) or []) > 1:
        hdr.append("Accept-Language")
    hdr.extend(res.variances(req, rsp))
    rsp.vary = hdr

    return res.resource_exists(req, rsp)

def g08(res, req, rsp):
    "If-Match exists?"
    return "if-match" in req.headers

def g09(res, req, rsp):
    "If-Match: * exists?"
    return '*' in req.if_match

def g11(res, req, rsp):
    "Etag in If-Match?"
    return res.generate_etag(req, rsp) in req.if_match

def h07(res, req, rsp):
    "If-Match: * exists?"
    return '*' in req.if_match

def h10(res, req, rsp):
    "If-Unmodified-Since exists?"
    return "if-unmodified-since" in req.headers

def h11(res, req, rsp):
    "If-Unmodified-Since is a valid date?"
    return req.if_unmodified_since is not None

def h12(res, req, rsp):
    "Last-Modified > If-Unmodified-Since?"
    rsp.last_modified = res.last_modified(req, rsp)
    return rsp.last_modified > req.if_unmodified_since

def i04(res, req, rsp):
    "Apply to a different URI?"
    uri = res.moved_permanently(req, rsp)
    if not uri:
        return False
    rsp.location = uri
    return True

def i07(res, req, rsp):
    "PUT?"
    return req.method == "PUT"

def i12(res, req, rsp):
    "If-None-Match exists?"
    return "if-none-match" in req.headers
    
def i13(res, req, rsp):
    "If-None-Match: * exists?"
    return '*' in req.if_none_match
    
def j18(res, req, rsp):
    "GET/HEAD?"
    return req.method in ["GET", "HEAD"]

def k05(res, req, rsp):
    "Resource moved permanently?"
    uri = res.moved_permanently(req, rsp)
    if not uri:
        return False
    rsp.location = uri
    return True

def k07(res, req, rsp):
    "Resource previously existed?"
    return res.previously_existed(req, rsp)

def k13(res, req, rsp):
    "Etag in If-None-Match?"
    return res.generate_etag(req, rsp) in req.if_none_match

def l05(res, req, rsp):
    "Resource moved temporarily?"
    return res.moved_temporarily(req, rsp)

def l07(res, req, rsp):
    "POST?"
    return req.method == "POST"

def l13(res, req, rsp):
    "If-Modified-Since exists?"
    return "if-modified-since" in req.headers

def l14(res, req, rsp):
    "If-Modified-Since is a valid date?"
    return req.if_modified_since is not None

def l15(res, req, rsp):
    "If-Modified-Since > Now?"
    return req.if_modified_since > datetime.datetime.now()

def l17(res, req, rsp):
    "Last-Modified > If-Modified-Since?"
    rsp.last_modified = res.last_modified(req, rsp)
    return rsp.last_modified > req.if_modified_since

def m05(res, req, rsp):
    "POST?"
    return req.method == "POST"

def m07(res, req, rsp):
    "Server permits POST to missing resource?"
    return res.allow_missing_post(req, rsp)

def m16(res, req, rsp):
    "DELETE?"
    return req.method == "DELETE"

def m20(res, req, rsp):
    "Delete enacted?"
    return res.delete_completed(req, rsp)

def n05(res, req, rsp):
    "Server permits POST to missing resource?"
    return res.allow_missing_post(req, rsp)

def n11(res, req, rsp):
    "Redirect?"
    if res.post_is_create(req, rsp):
        handle_request_body(res, req, rsp)
    elif not res.process_post(req, rsp):
        raise errors.ServerError("Failed to process POST body.")
    rsp.location = res.created_location(req, rsp)
    if rsp.location:
        return True
    return False

def n16(res, req, rsp):
    "POST?"
    return req.method == "POST"

def o14(res, req, rsp):
    "Is conflict?"
    return res.is_conflict(req, rsp)

def o16(res, req, rsp):
    "PUT?"
    return req.method == "PUT"

def o18(res, req, rsp):
    "Multiple representations? (Build GET/HEAD body)"
    if req.method not in ["GET", "HEAD"]:
        return res.multiple_choices(req, rsp)
    
    rsp.etag = res.generate_etag(req, rsp)
    rsp.last_modified = res.last_modified(req, rsp)
    rsp.expires = res.expires(req, rsp)
    
    func = [
        f for (ct, f)
        in res.content_types_provided(req, rsp) if ct == rsp.content_type
    ][0]
    
    rsp.app_iter = func(req, rsp)

    return res.multiple_choices(req, rsp)

def o20(res, req, rsp):
    "Response includes entity?"
    return req.app_iter is not None

def p03(res, req, rsp):
    "Conflict?"
    if res.is_conflict(req, rsp):
        return True
    handle_request_body(res, req, rsp)
    return False

def p11(res, req, rsp):
    "New resource?"
    return rsp.location is not None

def handle_request_body(res, req, rsp):
    ctype = req.content_type or "application/octet-stream"
    mtype = ctype.split(";", 1)[0]
    
    funcs = [
        f for (mt, f)
        in res.content_types_accepted(req, rsp) if mt == mtype
    ]
    if len(funcs) == 0:
        raise webob.exc.HTTPUnsupportedMediaType()
    
    return funcs[0](req, rsp)


TRANSITIONS = {
    b03: (200, c03), # Options?
    b04: (413, b03), # Request entity too large?
    b05: (415, b04), # Unknown Content-Type?
    b06: (501, b05), # Unknown or unsupported Content-* header?
    b07: (403, b06), # Forbidden?
    b08: (b07, 401), # Authorized?
    b09: (400, b08), # Malformed?
    b10: (b09, 405), # Is method allowed?
    b11: (414, b10), # URI too long?
    b12: (b11, 501), # Known method?
    b13: (b12, 503), # Service available?
    c03: (c04, d04), # Accept exists?
    c04: (d04, 406), # Acceptable media type available?
    d04: (d05, e05), # Accept-Language exists?
    d05: (e05, 406), # Accept-Language available?
    e05: (f06, e06), # Accept-Charset exists?
    e06: (f06, 406), # Acceptable charset available?
    f06: (f07, g07), # Accept-Encoding exists?
    f07: (g07, 406), # Acceptable encoding available?
    g07: (g08, h07), # Resource exists?
    g08: (g09, h10), # If-Match exists?
    g09: (h10, g11), # If-Match: * exists?
    g11: (h10, 412), # Etag in If-Match?
    h07: (412, i07), # If-Match: * exists?
    h10: (h11, i12), # If-Unmodified-Since exists?
    h11: (h12, i12), # If-Unmodified-Since is valid date?
    h12: (412, i12), # Last-Modified > If-Unmodified-Since?
    i04: (301, p03), # Apply to a different URI?
    i07: (i04, k07), # PUT?
    i12: (i13, l13), # If-None-Match exists?
    i13: (j18, k13), # If-None-Match: * exists?
    j18: (304, 412), # GET/HEAD?
    k05: (301, l05), # Resource moved permanently?
    k07: (k05, l07), # Resource previously existed?
    k13: (j18, l13), # Etag in If-None-Match?
    l05: (307, m05), # Resource moved temporarily?
    l07: (m07, 404), # POST?
    l13: (l14, m16), # If-Modified-Since exists?
    l14: (l15, m16), # If-Modified-Since is valid date?
    l15: (m16, l17), # If-Modified-Since > Now?
    l17: (m16, 304), # Last-Modified > If-Modified-Since?
    m05: (n05, 410), # POST?
    m07: (n11, 404), # Server permits POST to missing resource?
    m16: (m20, n16), # DELETE?
    m20: (o20, 202), # Delete enacted?
    n05: (n11, 410), # Server permits POST to missing resource?
    n11: (303, p11), # Redirect?
    n16: (n11, o16), # POST?
    o14: (409, p11), # Conflict?
    o16: (o14, o18), # PUT?
    o18: (300, 200), # Multiple representations?
    o20: (o18, 204), # Response includes entity?
    p03: (409, p11), # Conflict?
    p11: (201, o20)  # New resource?
}

def process(klass, req, rsp):
    res = klass(req, rsp)
    state = b13
    while not isinstance(state, int):
        if state(res, req, rsp):
            state = TRANSITIONS[state][0]
        else:
            state = TRANSITIONS[state][1]
        if not isinstance(state, (int, types.FunctionType)):
            raise webob.exc.HTTPServerError("Invalid state: %r" % state)
    rsp.status = state
