import t
from pywebmachine.conneg import BasicEntry, EncodingNegotiation, encoding_match

def eq(entry, name, qual):
    if isinstance(entry, str):
        entry = BasicEntry(entry)
    t.eq(entry.name, name)
    t.eq(entry.quality, qual)

def test_neg_simple():
    n = EncodingNegotiation("gzip, compress")
    t.eq(len(n.entries), 2)
    eq(n.entries[0], "gzip", 1.0)
    eq(n.entries[1], "compress", 1.0)
    t.eq(n.quality("gzip"), 1.0)
    t.eq(n.quality("compress"), 1.0)
    t.eq(n.quality("identity"), 0.0)
    t.eq(n.choose(["gzip"]), "gzip")
    t.eq(n.choose(["compress"]), "compress")
    t.eq(n.choose(["gzip", "compress"]), "gzip")

    # compress == gzip, which should be returned?
    # Going with compress to allow the app to decide
    # what it prefers to send. Or something.
    t.eq(n.choose(["compress", "gzip"]), "compress")

    # Identity is always ok
    t.eq(n.choose(["identity"]), "identity")

def test_neg_empty():
    n = EncodingNegotiation("")
    t.eq(len(n.entries), 0)
    t.eq(n.choose(["identity", "gzip"]), "identity")
    t.eq(n.choose(["gzip"]), None)

def test_neg_no_identity():
    n = EncodingNegotiation("identity;q=0")
    t.eq(n.choose(["identity"]), None)
    n = EncodingNegotiation("*;q=0")
    t.eq(n.choose(["idenitty"]), None)

def test_match():
    t.eq(encoding_match(["gzip", "compress"], "gzip;q=0.3"), "gzip")
    t.eq(encoding_match(["identity"], "compress;q=0.9"), "identity")