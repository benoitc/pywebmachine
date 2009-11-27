
from decisions import *
import errors

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
    g07: (g08, ho7), # Resource exists?
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
    n16: (n11, 016), # POST?
    o14: (409, p11), # Conflict?
    o16: (o14, o18), # PUT?
    o18: (300, 200), # Multiple representations?
    o20: (o18, 204), # Response includes entity?
    p03: (409, p11), # Conflict?
    p11: (201, o20)  # New resource?
}

def process(klass, wrq):
    res = resource_class(wrq)
    try:
        state = b13
        while True:
            result = state(res, req)
            if result:
                state = TRANSITIONS[state][0]
            else:
                state = TRANSITIONS[state][1]
            if isinstance(next_state, int):
                return next_state
            elif not isinstance(next_state, types.FunctionType):
                raise errors.InternalServerError("Invalid state: %r" % state)
    except errors.Halt:
        return inst.code
    except errors.PyWMError, inst:
        wrq.set_body(inst.mesg)
        return inst.code
