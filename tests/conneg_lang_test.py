import t
from pywebmachine.conneg import BasicEntry, CharsetNegotiation, charset_match

def eq(entry, name, qual):
    if isinstance(entry, str):
        entry = BasicEntry(entry)
    t.eq(entry.name, name)
    t.eq(entry.quality, qual)

def test_neg_no_star():
    n = CharsetNegotiation("en, en-gb;q=0.5")
    t.eq(len(n.entries), 2)
    eq(n.entries[0], "en", 1.0)
    eq(n.entries[1], "en-gb", 0.5)
    t.eq(n.quality("en"), 1.0)
    t.eq(n.quality("en-gb"), 0.5)
    t.eq(n.choose(["en", "en-gb"]), "en")
    t.eq(n.choose(["es"]), None)