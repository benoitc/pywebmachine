
import datetime

import conneg
import utils

def b03(res, req, rsp):
    "Options?"
    if req.method == 'OPTIONS':
        rsp.headers["OPTIONS"] = res.options(req, rsp)
        return True
    return False

def b04(res, req, rsp):
    "Request entity too large?"
    return res.valid_entity_length(req, rsp)

def b05(res, req, rsp):
    "Unknown Content-Type?"
    return res.known_content_type(req, rsp)

def b06(res, req, rsp):
    "Unknown or unsupported Content-* header?"
    return res.valid_content_headers(req, rsp)

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
    return res.ping() && res.service_available(req, rsp)

def c03(res, req, rsp):
    "Accept exists?"
    return "accept" in req.headers

def c04(res, req, rsp):
    "Acceptable media type available?"
    ctypes = [ctype for (ctype, func) in req.content_types_provided(req, rsp)]
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
    charsets = [cs for (cs, func) in res.charsets_provided(req, rsp)]
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
    if len(res.content_types_available(req, rsp)) > 1:
        hdr.append("Accept")
    if len(res.charsets_provided(req, rsp)) > 1:
        hdr.append("Accept-Charset")
    if len(res.encodings_provided(req, rsp)) > 1:
        hdr.append("Accept-Encoding")
    if len(res.languages_provided(req, rsp)) > 1:
        hdr.append("Accept-Language")
    hdr.extend(res.variances(req, rsp))
    rsp.vary = hdr

    return res.resouce_exists(req, rsp)

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
        uri = res.create_path(req, rsp)
        if not isinstance(uri, basestring):
            raise errors.ServerError("post_is_create w/o create_path")
    elif not res.process_post(req, rsp):
        raise errors.ServerError("Failed to process POST body.")
    if rsp.redirect:
        if not rsp.location:
            raise errors.ServerError("Redirect requested without Location set.")
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
    "Multiple representations?"
    return res.multiple_choices(req, rsp)

def o20(res, req, rsp):
    "Response includes entity?"
    return req.body is not None

def p03(res, req, rsp):
    "Conflict?"
    return res.is_conflict(req, rsp)

def p11(res, res, rsp):
    return rsp.location is not None
