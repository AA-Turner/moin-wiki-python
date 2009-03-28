import re

# -- version 1

class VersionParser(re.Scanner):
    tagmap = {'alpha': -30, 'a': -30,
              'beta': -20, 'b': -20,
              'rc': -10, 'c': -10}
    def __init__(self):
        re.Scanner.__init__(self, [(r'\d+', self.handle_number),
                                   (r'[a-z-]+', self.handle_tag),
                                   (r'[-.]', None)])
    def handle_number(self, s, n):
        return int(n)
    def handle_tag(self, s, t):
        if not self.had_tag:
            self.had_tag = True
            return self.tagmap.get(t, -40)
        raise ValueError('only one tag is allowed')
    def parse(self, version):
        self.had_tag = False
        self.tag_index = -1
        self.index = 0
        result, rest = self.scan(version)
        if rest:
            raise ValueError('%r unexpected in version' % rest)
        # strip out redundant '.0's
        a = b = len(result)
        for i, p in enumerate(result):
            if p < 0:
                if a == -1:
                    a = i
                b = i
                break
            elif p == 0:
                if a == -1:
                    a = i
            else:
                a = -1
        return result[:a], result[b:]

p = VersionParser().parse

# -- version 2

n_re = re.compile(r'\d+')
t_re = re.compile(r'[a-z-]+')
i_re = re.compile('[-.]+')

def parse_version(version):
    length = len(version)
    pos = 0
    n, t = [], []
    c = n
    while pos < length:
        m = n_re.match(version, pos)
        if m:
            c.append(int(m.group()))
            pos = m.end()
        else:
            m = t_re.match(version, pos)
            if m:
                if c is t:
                    raise ValueError('two tags')
                c = t
                c.append(VersionParser.tagmap.get(m.group(), -40))
                pos = m.end()
            else:
                m = i_re.match(version, pos)
                if m:
                    pos = m.end()
                else:
                    raise ValueError('unexpected char')
    while n[-1] == 0:
        n.pop()
    return n, t

q = parse_version
