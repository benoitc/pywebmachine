import t
from pywebmachine.conneg import BasicEntry, BasicNegotiation

def eq(entry, name, qual):
    if isinstance(entry, str):
        entry = BasicEntry(entry)
    t.eq(entry.name, name)
    t.eq(entry.quality, qual)

def test_basic():
    eq("baz", "baz", 1.0)
    eq("bam;q=0.2", "bam", 0.2)
    eq("zim;q=0.4", "zim", 0.4)
    eq("foo;q", "foo", 0.0)
    eq("foo;q=0.1;f=3", "foo", 0.1)

def test_neg_split_one():
    n = BasicNegotiation("zim")
    t.eq(len(n.entries), 1)
    eq(n.entries[0], "zim", 1.0)

def test_neg_split_multi():
    n = BasicNegotiation("zib, jab;q=0.3, jim")
    t.eq(len(n.entries), 3)
    eq(n.entries[0], "zib", 1.0)
    eq(n.entries[1], "jab", 0.3)
    eq(n.entries[2], "jim", 1.0)

def test_neg_split_star():
    n = BasicNegotiation("zoo;q=0.1, *;q=0.3")
    t.eq(len(n.entries), 2)
    eq(n.entries[0], "zoo", 0.1)
    eq(n.entries[1], "*", 0.3)

def test_neg_no_star():
    n = BasicNegotiation("zib;q=0.6")
    t.eq(len(n.entries), 1)
    eq(n.entries[0], "zib", 0.6)
    t.eq(n.quality("zib"), 0.6)
    t.eq(n.quality("millions"), 0.0)
    t.eq(n.choose(["zib"]), "zib")
    t.eq(n.choose(["zab"]), None)
    t.eq(n.choose(["zab", "zib"]), "zib")

def test_neg_star():
    n = BasicNegotiation("zing, *;q=0.9")
    t.eq(len(n.entries), 2)
    eq(n.entries[0], "zing", 1.0)
    eq(n.entries[1], "*", 0.9)
    t.eq(n.quality("zing"), 1.0)
    t.eq(n.quality("grim"), 0.9)
    t.eq(n.quality("grab"), 0.9)
    t.eq(n.choose(["zing"]), "zing")
    t.eq(n.choose(["grim"]), "grim")
    t.eq(n.choose(["grab"]), "grab")
    t.eq(n.choose(["zing", "grim"]), "zing")
    t.eq(n.choose(["zing", "grab"]), "zing")
