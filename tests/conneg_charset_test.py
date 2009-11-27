import t
from pywebmachine.conneg import BasicEntry, CharsetNegotiation, charset_match

def eq(entry, name, qual):
    if isinstance(entry, str):
        entry = BasicEntry(entry)
    t.eq(entry.name, name)
    t.eq(entry.quality, qual)

def test_neg_no_star():
    n = CharsetNegotiation("utf-8;q=0.6")
    t.eq(len(n.entries), 1)
    eq(n.entries[0], "utf-8", 0.6)
    t.eq(n.quality("utf-8"), 0.6)
    t.eq(n.quality("iso-8859-1"), 1.0)
    t.eq(n.quality("latin-1"), 0.0)
    t.eq(n.choose(["utf-8"]), "utf-8")
    t.eq(n.choose(["iso-8859-1"]), "iso-8859-1")
    t.eq(n.choose(["utf-8", "iso-8859-1"]), "iso-8859-1")
    t.eq(n.choose(["latin-1"]), None)

def test_neg_star():
    n = CharsetNegotiation("utf-8, *;q=0.9")
    t.eq(len(n.entries), 2)
    eq(n.entries[0], "utf-8", 1.0)
    eq(n.entries[1], "*", 0.9)
    t.eq(n.quality("utf-8"), 1.0)
    t.eq(n.quality("iso-8859-1"), 0.9)
    t.eq(n.quality("latin-1"), 0.9)
    t.eq(n.choose(["utf-8"]), "utf-8")
    t.eq(n.choose(["iso-8859-1"]), "iso-8859-1")
    t.eq(n.choose(["latin-1"]), "latin-1")
    t.eq(n.choose(["utf-8", "iso-8859-1"]), "utf-8")
    t.eq(n.choose(["utf-8", "latin-1"]), "utf-8")

def test_match():
    t.eq(charset_match(["utf-8"], "*;0.3"), "utf-8")
    t.eq(charset_match(["iso-8859-1"], "utf-8"), "iso-8859-1")