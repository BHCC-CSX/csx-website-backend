class URLHook:
    def __init__(self, patterns):
        self.pats = patterns


class NamedURLHook:
    def __init__(self, patterns, prefix):
        self.pats = patterns
        self.prefix = prefix
