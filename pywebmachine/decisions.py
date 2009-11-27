
import datetime

import conneg
import utils

def b03(res, wrq):
    "Options?"
    if wrq.method().upper() == "OPTIONS":
        req.set_response_header(res.options())
        return True
    return False

def b04(res, wrq):
    "Request entity too large?"
    return res.valid_entity_length()

def b05(res, wrq):
    "Unknown Content-Type?"
    return res.known_content_type()

def b06(res, wrq):
    "Unknown or unsupported Content-* header?"
    return res.valid_content_headers()

def b07(res, wrq):
    "Forbidden?"
    return res.forbidden()

def b08(res, wrq):
    "Authorized?"
    resp = res.is_authorized()
    if resp is True:
        return True
    elif isinstance(resp, basestring):
        wrq.set_response_header("WWW-Authenticate", resp)
    return False

def b09(res, wrq):
    "Malformed?"
    return res.malformed_request()

def b10(res, wrq):
    "Is method allowed?"
    return wrq.method().upper() in res.allowed_methods()

def b11(res, wrq):
    "URI too long?"
    return res.uri_too_long()

def b12(res, wrq):
    "Known method?"
    return wrq.method().upper() in res.allowed_methods()

def b13(res, wrq):
    "Service available?"
    return res.ping() && res.service_available()

def c03(res, wrq):
    "Accept exists?"
    return wrq.get_header("accept") is not None:

def c04(res, wrq):
    "Acceptable media type available?"
    ctypes = [ctype for (ctype, func) in req.content_types_provided(wrq)]
    ctype = conneg.accept_match(ctypes, wrq.get_header('accept'))
    if ctype is None:
        return False
    wrq.set_meta("content-type", ctype)
    return True

def d04(res, wrq):
    "Accept-Language exists?"
    return wrq.get_header('accept-language') is not None

def d05(res, wrq):
    "Accept-Language available?"
    (langs, wrq) = res.languages_available(wrq)
    lang = conneg.language_match(langs, wrq.get_header("accept-language"))
    if lang is None:
        return False
    wrq.set_meta("language", lang)
    return True
    
def e05(res, wrq):
    "Accept-Charset exists?"
    return wrq.get_header("accept-charset") is not None

def e06(res, wrq):
    "Acceptable charset available?"
    (charsets, wrq) = res.charsets_provided(wrq)
    charset = conneg.charset_match(charsets, wrq.get_header("accept-charset"))
    if charset is None:
        return False
    wrq.set_meta("charset", charset)

    # Set the content-type now that we know it.
    ctype = wrq.get_meta("content-type") + "; " + charset
    wrq.set_response_header("Content-Type", ctype)

    return True

def f06(res, wrq):
    "Accept-Encoding exists?"
    return wrq.get_header("accept-encoding") is not None

def f07(res, wrq):
    "Acceptable encoding available?"
    (encodings, wrq) = res.charsets_provided(wrq)
    enc = conneg.encoding_match(encodings, wrq.get_header("accept-encodings"))
    if enc is None:
        return False
    wrq.set_meta("encoding", enc)
    return True

def g07(res, wrq):
    "Resource exists?"

    # Set variances now that conneg is done
    hdr = []
    if len(res.content_types_available()) > 1:
        hdr.append("Accept")
    if len(res.charsets_provided()) > 1:
        hdr.append("Accept-Charset")
    if len(res.encodings_provided()) > 1:
        hdr.append("Accept-Encoding")
    if len(res.languages_provided()) > 1:
        hdr.append("Accept-Language")
    hdr.extend(res.variances())
    wrq.set_response_header("Vary", ", ".join(hdr))

    return res.resouce_exists()

def g08(res, wrq):
    "If-Match exists?"
    return wrq.get_header("if-match") is not None

def g09(res, wrq):
    "If-Match: * exists?"
    return "*" in wrq.get_header_list("if-match")

def g11(res, wrq):
    "Etag in If-Match?"
    return res.generate_etag() in res.get_header_list("if-match")

def h07(res, wrq):
    "If-Match: * exists?"
    return "*" in wrq.get_header_list("if-match")

def h10(res, wrq):
    "If-Unmodified-Since exists?"
    return wrq.get_header("if-unmodified-since") is not None

def h11(res, wrq):
    "If-Unmodified-Since is a valid date?"
    try:
        since = utils.parse_date(wrq.get_header("if-unmodified-since"))
        wrq.set_meta("unmodified-since", since)
        return True
    except:
        return False

def h12(res, wrq):
    "Last-Modified > If-Unmodified-Since?"
    since = wrq.get_meta("unmodified-since")
    last = res.last_modified()
    wrq.set_response_header("Last-Modified", utils.to_http_date_str(last))
    return last > since

def i04(res, wrq):
    "Apply to a different URI?"
    uri = res.moved_permanently()
    if isinstance(uri, basestring):
        wrq.set_response_header("Location", uri)
        return True
    return False

def i07(res, wrq):
    "PUT?"
    return wrq.method().upper() == "PUT"

def i12(res, wrq):
    "If-None-Match exists?"
    return wrq.get_header("if-none-match") is not None
    
def i13(res, wrq):
    "If-None-Match: * exists?"
    return "*" in wrq.get_header_list("if-none-match")

def j18(res, wrq):
    "GET/HEAD?"
    return wrq.method().upper() in ["GET", "HEAD"]

def k05(res, wrq):
    "Resource moved permanently?"
    uri = res.moved_permanently()
    if isinstance(result, basestring):
        wrq.set_response_header("Location", uri)
        return True
    return False

def k07(res, wrq):
    "Resource previously existed?"
    return res.previously_existed()

def k13(res, wrq):
    "Etag in If-None-Match?"
    return res.generate_etag() in wrq.get_header_list("if-none-match")

def l05(res, wrq):
    "Resource moved temporarily?"
    return res.moved_temporarily()

def l07(res, wrq):
    "POST?"
    return wrq.method().upper() == "POST"

def l13(res, wrq):
    "If-Modified-Since exists?"
    return wrq.get_header("if-modified-since") is not None

def l14(res, wrq):
    "If-Modified-Since is a valid date?"
    try:
        since = utils.parse_date(wrq.get_header("if-modified-since"))
        wrq.set_meta("modified-since", since)
        return True
    except:
        return False

def l15(res, wrq):
    "If-Modified-Since > Now?"
    since = wrq.get_meta("modified-since")
    now = datetime.datetime.now()
    return since > now

def l17(res, wrq):
    "Last-Modified > If-Modified-Since?"
    since = wrq.get_meta("modified-since")
    last = res.last_modified()
    wrq.set_response_header("Last-Modified", utils.to_http_date_str(last))
    return last > since

def m05(res, wrq):
    "POST?"
    return wrq.method().upper() == "POST"

def m07(res, wrq):
    "Server permits POST to missing resource?"
    return res.allow_missing_post()

def m16(res, wrq):
    "DELETE?"
    return wrq.method().upper() == "DELETE"

def m20(res, wrq):
    "Delete enacted?"
    return res.delete_completed()

def n05(res, wrq):
    "Server permits POST to missing resource?"
    return res.allow_missing_post()

def n11(res, wrq):
    "Redirect?"
    if res.post_is_create():
        uri = res.create_path()
        if not isinstance(uri, basestring):
            raise errors.ServerError("post_is_create w/o create_path")
    elif not res.process_post():
        raise errors.ServerError("Failed to process POST body.")
    if wrq.is_redirect():
        if wrq.get_response_header("Location") is None:
            raise errors.ServerError("Redirect requested without Location set.")
        return True
    return False

def n16(res, wrq):
    "POST?"
    return wrq.method().upper() == "POST"

def o14(res, wrq):
    "Is conflict?"
    return res.is_conflict()

def o16(res, wrq):
    "PUT?"
    return wrq.method().upper() == "PUT"

def o18(res, wrq):
    "Multiple representations?"
    return res.multiple_choices()

def o20(res, wrq):
    "Response includes entity?"
    return wrq.has_body()

def p03(res, wrq):
    "Conflict?"
    return wrq.is_conflict()

def p11(res, wrq):
    return wrq.get_response_header("Location") is not None
