
import t
from pywebmachine.conneg import AcceptEntry, AcceptNegotiation, accept_match

def eq(entry, type, subtype, qual, params):
    if isinstance(entry, str):
        entry = AcceptEntry(entry)
    t.eq(entry.type, type)
    t.eq(entry.subtype, subtype)
    t.eq(entry.quality, qual)
    t.eq(entry.params, params)

def test_basic():
    eq('text/xml', 'text', 'xml', 1.0, {})

def test_wildcards():
    eq("*", "*", "*", 1.0, {})
    eq('*/*', '*', '*', 1.0, {})
    eq('*/xml', '*', 'xml', 1.0, {})
    eq('text/*', 'text', '*', 1.0, {})

def test_parameters():
    eq('text/xml;level=2', 'text', 'xml', 1.0, {'level': '2'})
    eq('text/xml;level=baz', 'text', 'xml', 1.0, {'level': 'baz'})

def test_escaping():
    eq('text/xml;level="f b"', 'text', 'xml', 1.0, {'level': '"f b"'})
    eq('text/xml;level="f\\\"b"', 'text', 'xml', 1.0, {'level': '"f\\\"b"'})
    
def test_qualities():
    eq('text/xml; q=0.45', 'text', 'xml', 0.45, {})
    eq('text/xml;q=1.5', 'text', 'xml', 1.0, {})
    eq('text/xml;q=-1.0', 'text', 'xml', 0.0, {})
    eq('text/xml;q=foo', 'text', 'xml', 0.0, {})

def test_multiple_parameters():
    eq('text/xml;q=0.3;level=baz', 'text', 'xml', 0.3, {'level': 'baz'})
    eq('text/xml;q=0.2; level="f b"', 'text', 'xml', 0.2, {'level': '"f b"'})
    eq('text/xml;q=0.5 ;level="s;h"', 'text', 'xml', 0.5, {'level': '"s;h"'})
    eq('text/xml;q=0.3  ;  level=","', 'text', 'xml', 0.3, {'level': '","'})
    eq('text/xml;q=0.2 ; q=0.0', 'text', 'xml', 0.2, {})

def test_neg_single():
    n = AcceptNegotiation('text/xml')
    t.eq(len(n.entries), 1)
    eq(n.entries[0], 'text', 'xml', 1.0, {})

def test_neg_split():
    n = AcceptNegotiation('text/xml, text/*')
    t.eq(len(n.entries), 2)
    eq(n.entries[0], 'text', 'xml', 1.0, {})
    eq(n.entries[1], 'text', '*', 1.0, {})

def test_neg_split_params():
    n = AcceptNegotiation('text/xml;q=0.3, */plain;level=3')
    t.eq(len(n.entries), 2)
    eq(n.entries[0], 'text', 'xml', 0.3, {})
    eq(n.entries[1], '*', 'plain', 1.0, {'level': '3'})

def test_neg_split_escaped():
    n = AcceptNegotiation('text/xml;q=0.2;level="f,b",image/jpeg')
    t.eq(len(n.entries), 2)
    eq(n.entries[0], 'text', 'xml', 0.2, {'level': '"f,b"'})
    eq(n.entries[1], 'image', 'jpeg', 1.0, {})

def test_neg_drop():
    n = AcceptNegotiation('text/plain;q=0.0')
    t.eq(len(n.entries), 0)

def test_neg_drop_one():
    n = AcceptNegotiation('text/plain, image/jpeg;q=0, application/json;q=0.1')
    t.eq(len(n.entries), 2)
    eq(n.entries[0], 'text', 'plain', 1.0, {})
    eq(n.entries[1], 'application', 'json', 0.1, {})

def test_neg_qualities():
    value = """
        text/*;q=0.3, text/html;q=0.7, text/html;level=1,
        text/html;level=2;q=0.4, */*;q=0.5
    """
    n = AcceptNegotiation(value)
    t.eq(n.quality('text/html;level=1'), 1.0)
    t.eq(n.quality('text/html'), 0.7)
    t.eq(n.quality('text/plain'), 0.3)
    t.eq(n.quality('image/jpeg'), 0.5)
    t.eq(n.quality('text/html;level=2'), 0.4)
    t.eq(n.quality('text/html;level=3'), 0.7)
    
def test_neg_choose():
    supported = ["text/html", "text/plain"]
    t.eq(accept_match(supported, "text/html"), "text/html")
    t.eq(accept_match(supported, "text/html;q=1"), "text/html")
    t.eq(accept_match(supported, "text/plain"), "text/plain")

    # I'm different than mimeparse.py here. As I read the RFC,
    # the first appearance of equal matches should be preferred.
    t.eq(accept_match(supported, "*/*"), "text/html")
    t.eq(accept_match(supported, "text/*"), "text/html")

def test_neg_prefer_specific():
    supported = ["text/xml", "image/jpeg"]
    t.eq(accept_match(supported, "*/xml"), "text/xml")
    t.eq(accept_match(supported, "*/jpeg"), "image/jpeg")
    t.eq(accept_match(supported, "image/*;q=0.6, */xml;q=0.5"), "image/jpeg")
    t.eq(accept_match(supported, "image/*;q=0.5, */xml;q=0.6"), "text/xml")

def test_neg_no_match():
    supported = ["text/html", "text/plain"]
    t.eq(accept_match(supported, "image/plain"), None)

def test_ajax():
    supported = ["application/json", "text/xml"]
    t.eq(
        accept_match(supported, "application/json, text/javascript, */*"),
        "application/json"
    )
    t.eq(
        accept_match(supported, "application/json, text/xml;q=0.8"),
        "application/json"
    )


