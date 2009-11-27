
from decisions import *

TRANSITIONS = {
    b3: (200, c3),    # Options?
    b4: (413, b3),    # Request entity too large?
    b5: (415, b4),    # Unknown Content-Type?
    b6: (501, b5),    # Unknown or unsupported Content-* header?
    b7: (403, b6),    # Forbidden?
    b8: (b7, 401),    # Authorized?
    b9: (400, b8),    # Malformed?
    b10: (b9, 405),   # Is method allowed?
    b11: (414, b10),  # URI too long?
    b12: (b11, 501),  # Known method?
    b13: (b13b, 503), # Ping?
    b13b: (b12, 503), # Service available?
    c3: (c4, d4),     # Accept exists?
    c4: (d4, 406),    # Acceptable media type available?
    d4: (d5, e5),     # Accept-Language exists?
    d5: (e5, 406),    # Accept-Language available?
    e5: (f6, e6),     # Accept-Charset exists?
    e6: (f6, 406),    # Acceptable charset available?
    f6: (f7, g7),     # Accept-Encoding exists?
    f7: (g7, 406),    # Acceptable encoding available?
    g7: (g8, h7),     # Resource exists?
    g8: (g9, h10),    # If-Match exists?
    g9: (h10, g11),   # If-Match: * exists?
    g11: (h10, 412),  # Etag in If-Match?
    h7: (412, i7),    # If-Match: * exists?
    h10: (h11, i12),  # If-Unmodified-Since exists?
    h11: (h12, i12),  # If-Unmodified-Since is valid date?
    h12: (412, i12),  # Last-Modified > If-Unmodified-Since?
    i4: (301, p3),    # Apply to a different URI?
    i7: (i4, k7),     # PUT?
    i12: (i13, l13),  # If-None-Match exists?
    i13: (j18, k13),  # If-None-Match: * exists?
    j18: (304, 412),  # GET/HEAD?
    k5: (301, l5),    # Resource moved permanently?
    k7: (k5, l7),     # Resource previously existed?
    k13: (j18, l13),  # Etag in If-None-Match?
    l5: (307, m5),    # Resource moved temporarily?
    l7: (m7, 404),    # POST?
    l13: (l14, m16),  # If-Modified-Since exists?
    l14: (l15, m16),  # If-Modified-Since is valid date?
    l15: (m16, l17),  # If-Modified-Since > Now?
    l17: (m16, 304),  # Last-Modified > If-Modified-Since?
    m5: (n5, 410),    # POST?
    m7: (n11, 404),   # Server permits POST to missing resource?
    m16: (m20, n16),  # DELETE?
    m20: (o20, 202),  # Delete enacted?
    n5: (n11, 410),   # Server permits POST to missing resource?
    n11: (303, p11),  # Redirect?
    n16: (n11, 016),  # POST?
    o14: (409, p11),  # Conflict?
    o16: (o14, o18),  # PUT?
    o18: (300, 200),  # Multiple representations?
    o20: (o18, 204),  # Response includes entity?
    p3: (409, p11),   # Conflict?
    p11: (201, o20)   # New resource?
}