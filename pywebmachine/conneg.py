
import re

import errors

media_range = re.compile("^(\*|\S+)/(\*|\S+)$")

def quoted_split(value, delim):
    """\
    Split a string on ``delim`` while ignoring instances that
    occur in quoted strings.
    """
    parts = []
    def next_bit(rem):
        pos = 0
        while pos < len(value) and value[pos] != delim:
            if value[pos] == '"':
                pos += 1
                while pos < len(value) and value[pos] != '"':
                    pos += 1
                    if pos < len(value) and value[pos] == "\\":
                        pos += 2
            pos += 1
        return rem[:pos].strip(), rem[pos+1:]
    while value:
        (bit, value) = next_bit(value)
        if bit:
            parts.append(bit)
    return parts


class Entry(object):
    def match(self, value):
        raise NotImplemented

class ContentNegotiation(object):
    def __init__(self, value):
        entries = map(self.EntryClass, self.split(value))
        self.entries = [e for e in entries if e.quality > 0.0]

    def split(self, value):
        raise NotImplemented

    def quality(self, mimetype):
        entry = self.EntryClass(mimetype)
        best = (-1, 0.0)
        for e in self.entries:
            curr = e.match(entry)
            if curr[0] > best[0]:
                best = curr
        return best[1]

    def choose(self, supported):
        scored = []
        for s in supported:
            scored.append((s, self.quality(s)))
        best = (None, 0.0)
        for s in scored:
            if s[1] > best[1]:
                best = s
        return best[0]


class BasicEntry(Entry):
    def __init__(self, value):
        bits = value.split(";")
        self.name = bits[0].strip()
        self.quality = 1.0
        for b in bits[1:]:
            b = b.split("=", 1)
            if b[0].strip() == "q":
                try:
                    qual = float(b[-1])
                except:
                    qual = 0.0
                self.quality = max(min(qual, 1.0), 0.0)
                break
    
    def match(self, other):
        if self.name != "*" and self.name == other.name:
            return (1.0, self.quality)
        elif self.name == "*" or other.name == "*":
            return (0.5, self.quality)
        else:
            return (-1, 0.0)

class BasicNegotiation(ContentNegotiation):
    EntryClass = BasicEntry

    def split(self, value):
        return value.split(",")


class CharsetNegotiation(BasicNegotiation):
    def quality(self, value):
        entry = self.EntryClass(value)
        for e in self.entries:
            if e.name == entry.name:
                return e.quality
        for e in self.entries:
            if e.name == "*":
                return e.quality
        if entry.name.lower() == "iso-8859-1":
            return 1.0
        return 0.0

def charset_match(supported, requested):
    return CharsetNegotiation(requested).choose(supported)


class EncodingNegotiation(BasicNegotiation):
    def __init__(self, value):
        self.default = "identity"
        if value.strip():
            entries = map(self.EntryClass, self.split(value))
            for e in entries:
                if e.name == "identity" and e.quality == 0.0:
                    self.default = None
            self.entries = [e for e in entries if e.quality > 0.0]
        else:
            self.entries = []

    def choose(self, supported):
        scored = []
        for s in supported:
            scored.append((s, self.quality(s)))
        default = self.default
        if default not in supported:
            default = None
        best = (default, 0.0)
        for s in scored:
            if s[1] > best[1]:
                best = s
        return best[0]

def encoding_match(supported, requested):
    return EncodingNegotiation(requested).choose(supported)


class LanguageEntry(BasicEntry):
    def __init__(self, value):
        BasicEntry.__init__(self, value)
        self.name = self.name.split("-")

    def match(self, other):
        score = 0
        for i in range(min(len(self.name), len(other.name))):
            if self.name[i] == other.name[i]:
                score += len(self.name[i])
        return (score, self.quality)
            
class LanguageNegotiation(BasicNegotiation):
    EntryClass = LanguageEntry
        
def language_match(supported, requested):
    return LanguageNegotiation(requested).choose(supported)


class AcceptEntry(Entry):
    def __init__(self, value):
        bits = value.split(";", 1)
        if len(bits) == 1:
            media, params = bits[0].strip(), ""
        else:
            media, params = bits[0].strip(), bits[1].strip()
        # Following mimeparse.py to correct for Java's behavior
        if media == "*":
            media = "*/*"
        match = media_range.match(media)
        if not match:
            mesg = "Bad media-range in Accept: %r" % media
            raise errors.MalformedRequest(mesg)
        self.type, self.subtype = match.group(1), match.group(2)
        params = quoted_split(params, ';')
        self.params = {}
        for p in params:
            bits = p.split("=", 1)
            if len(bits) == 1:
                key, value = bits[0].strip(), None
            else:
                key, value = bits[0].strip(), bits[1].strip()
            if key == "q" and key in self.params:
                # q should be the first parameter, ignore repeated values
                continue
            elif key == "q":
                try:
                    value = float(value)
                except:
                    value = 0.0
            self.params[key] = value
        qual = self.params.pop("q", 1.0)
        self.quality = max(min(qual, 1.0), 0.0)

    def match(self, other):
        def compatible(a, b):
            return a == b or a == "*" or b == "*"
        if not compatible(self.type, other.type):
            return (-1, 0.0)
        if not compatible(self.subtype, other.subtype):
            return (-1, 0.0)
        score = 0
        if self.type != "*" and self.type == other.type:
            score += 1000
        if self.subtype != "*" and self.subtype == other.subtype:
            score += 100
        for p in other.params:
            if p in self.params and other.params[p] == self.params[p]:
                score += 1
        return (score, self.quality)

class AcceptNegotiation(ContentNegotiation):
    EntryClass = AcceptEntry

    def split(self, value):
        return quoted_split(value, ",")

def accept_match(supported, requested):
    return AcceptNegotiation(requested).choose(supported)

