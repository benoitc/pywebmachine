
import conneg
import utils

def check(resp):
    if not isinstance(resp, tuple):
        raise TypeError("Invalid resource response: %r" % resp)
    if len(resp) != 2:
        raise ValueError("Invalid resource response length: %s" % len(resp))
    if not isinstance(resp[0], bool):
        raise TypeError("Invalid resource response status: %r" % resp[0])
    if not isinstance(resp[1], WebRequest):
        raise TypeError("Invalid resource response webrequest: %r" % resp[1])
    return resp

def b3(res, wrq):
    "Options?"
    if wrq.method().upper() == "OPTIONS":
        return (True, wrq.set_headers(res.options(wrq)))
    return (False, wrq)

def b4(res, wrq):
    "Request entity too large?"
    return (res.valid_entity_length(wrq))

def b5(res, wrq):
    "Unknown Content-Type?"
    return (res.known_content_type(wrq))

def b6(res, wrq):
    "Unknown or unsupported Content-* header?"
    return (res.valid_content_headers(wrq))

def b7(res, wrq):
    "Forbidden?"
    return (res.forbidden(wrq))

def b8(res, wrq):
    "Authorized?"
    (resp, wrq) = res.is_authorized(wrq)
    if resp is True:
        return (True, wrq)
    if isinstance(resp, basestring):
        return (False, wrq.set_header("WWW-Authenticate", resp))
    return (False, wrq)

def b9(res, wrq):
    "Malformed?"
    return (res.malformed_request(wrq))

def b10(res, wrq):
    "Is method allowed?"
    (methods, wrq) = res.allowed_methods(wrq)
    return (wrq.method() in methods, wrq)

def b11(res, wrq):
    "URI too long?"
    return (res.uri_too_long(wrq))

def b12(res, wrq):
    "Known method?"
    (methods, wrq) = res.allowed_methods(wrq)
    return (wrq.method() in methods, wrq)

def b13(res, wrq):
    "Ping?"
    return (res.ping(wrq))

def b13b(res, wrq):
    "Service available?"
    return (res.service_available(wrq))

def c3(res, wrq):
    "Accept exists?"
    if wrq.get_header("accept"):
        return (True, wrq)
    return (False, wrq)

def c4(res, wrq):
    "Acceptable media type available?"
    ctypes = [ctype for (ctype, func) in req.content_types_provided(wrq)]
    ctype = conneg.accept_match(ctypes, wrq.get_header('accept'))
    if ctype:
        return (True, wrq.response_content_type(ctype))
    return (False, wrq)

def d4(res, wrq):
    "Accept-Language exists?"
    if wrq.get_header('accept-language'):
        return (True, wrq)
    return (False, wrq)

def d5(res, wrq):
    "Accept-Language available?"
    (langs, wrq) = res.languages_available(wrq)
    lang = conneg.language_match(langs, wrq.get_header("accept-language"))
    if lang:
        return (True, wrq.response_language(lang))
    return (False, wrq)
    
def e5(res, wrq):
    "Accept-Charset exists?"
    if wrq.get_header("accept-charset"):
        return (True, wrq)
    return (False, wrq)

def e6(res, wrq):
    "Acceptable charset available?"
    (charsets, wrq) = res.charsets_provided(wrq)
    charset = conneg.charset_match(charsets, wrq.get_header("accept-charset"))
    if charset:
        wrq = wrq.response_charset(lang)
        header = wrq.response_content_type() + "; " + charset
        return (True, wrq.set_response_header("Content-Type", header))
    return (False, wrq)

def f6(res, wrq):
    "Accept-Encoding exists?"
    if wrq.get_header("accept-encoding"):
        return (True, wrq)
    return (False, wrq)

def f7(res, wrq):
    "Acceptable encoding available?"
    (encodings, wrq) = res.charsets_provided(wrq)
    enc = conneg.encoding_match(encodings, wrq.get_header("accept-encodings"))
    if enc:
        return (True, wrq.response_encoding(enc))
    return (False, wrq)

def variances(res, wrq):
    (ctypes, ignore) = res.content_types_provided(wrq)
    (charsets, ignore) = res.charsets_provided(wrq)
    (encodings, ignore) = res.encodings_provided(wrq)
    (langs, ignore) = res.languages_provided(wrq)
    ret = []
    if len(ctypes) > 1:
        ret.append("Accept")
    if len(charsets) > 1:
        ret.append("Accept-Charset")
    if len(encodings) > 1:
        ret.append("Accept-Encoding")
    if len(langs) > 1:
        ret.append("Accept-Language")
    (variances, wrq) = res.variances(wrq)
    ret.extend(variances)
    return (', '.join(ret), wrq)

def g7(res, wrq):
    "Resource exists?"
    # Set variances now that conneg is done
    (header, wrq) = variances(res, wrq)
    wrq = wrq.set_response_header("Vary", header)

    return res.resource_exists(wrq)
    
def g8(res, wrq):
    "If-Match exists?"
    return (wrq.get_header("if-match") is not None, wrq)

def g9(res, wrq):
    "If-Match: * exists?"
    return (wrq.get_header("if-match") == "*", wrq)

def g11(res, wrq):
    "Etag in If-Match?"
    (etag, wrq) = res.generate_etag(wrq)
    if etag in res.get_header_list("if-match"):
        return (True, wrq)
    return (False, wrq)

def h7(res, wrq):
    "If-Match: * exists?"
    return (wrq.get_header("if-match") == "*", wrq)


def h10(res, wrq):
    "If-Unmodified-Since exists?"
    return (wrq.get_header("if-unmodified-since") is not None, wrq)

def h11(res, wrq):
    "If-Unmodified-Since is a valid date?"
    try:
        utils.parse_date(wrq.get_header("if-unmodified-since"))
        return (True, wrq)
    except:
        return (False, wrq)

def h12(res, wrq):
    "Last-Modified > If-Unmodified-Since?"
    since = utils.parse_date(wrq.get_header("if-unmodified-since"))
    (last, wrq) = res.last_modified(wrq)
    header = utils.to_http_date_str(last)
    return (last > since, wrq.set_response_header("Last-Modified", header))

    # i4: (301, p3),    # Apply to a different URI?
    # i7: (i4, k7),     # PUT?
    # i12: (i13, l13),  # If-None-Match exists?
    # i13: (j18, k13),  # If-None-Match: * exists?
    # j18: (304, 412),  # GET/HEAD?
    # k5: (301, l5),    # Resource moved permanently?
    # k7: (k5, l7),     # Resource previously existed?
    # k13: (j18, l13),  # Etag in If-None-Match?
    # l5: (307, m5),    # Resource moved temporarily?
    # l7: (m7, 404),    # POST?
    # l13: (l14, m16),  # If-Modified-Since exists?
    # l14: (l15, m16),  # If-Modified-Since is valid date?
    # l15: (m16, l17),  # If-Modified-Since > Now?
    # l17: (m16, 304),  # Last-Modified > If-Modified-Since?
    # m5: (n5, 410),    # POST?
    # m7: (n11, 404),   # Server permits POST to missing resource?
    # m16: (m20, n16),  # DELETE?
    # m20: (o20, 202),  # Delete enacted?
    # n5: (n11, 410),   # Server permits POST to missing resource?
    # n11: (303, p11),  # Redirect?
    # n16: (n11, 016),  # POST?
    # o14: (409, p11),  # Conflict?
    # o16: (o14, o18),  # PUT?
    # o18: (300, 200),  # Multiple representations?
    # o20: (o18, 204),  # Response includes entity?
    # p3: (409, p11),   # Conflict?
    # p11: (201, o20)   # New resource?
