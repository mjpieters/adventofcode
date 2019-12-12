import enum
import os.path
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

Net = enum.Enum('Net', 'HYPERNET SUPERNET')


class _Token:
    def __init__(self, value, net):
        self.value = value
        self.net = net

    def is_abba(self, _pat=re.compile(r'([a-z])([a-z])\2\1')):
        candidate = _pat.search(self.value)
        return bool(candidate and candidate.group(1) != candidate.group(2))

    def abas(self, _pat=re.compile(r'([a-z])(?=([a-z])\1)')):
        for candidate in _pat.finditer(self.value):
            if candidate.group(1) != candidate.group(2):
                yield candidate.group(1, 2)


class Hostname:
    def __init__(self, hostname):
        self.hostname = hostname

    def _tokens(self, _tokenize=re.compile(r'([\[\]])').split):
        inside_brackets = False
        for token in _tokenize(self.hostname):
            if token == '[':
                inside_brackets = True
            elif token == ']':
                inside_brackets = False
            else:
                yield _Token(
                    token, Net.HYPERNET if inside_brackets else Net.SUPERNET)

    def supports_tls(self):
        found_abba = False
        for token in self._tokens():
            if token.is_abba():
                if token.net is Net.HYPERNET:
                    return False
                found_abba = True
        return found_abba

    def supports_ssl(self):
        aba_candidates = []
        hypernet_sequences = []
        for token in self._tokens():
            if token.net is Net.SUPERNET:
                aba_candidates.extend(token.abas())
            else:
                hypernet_sequences.append(token)
        for aba in aba_candidates:
            bab = aba[::-1]
            if any(bab in token.abas() for token in hypernet_sequences):
                return True
        return False


def test(hostname, expected, m):
    result = getattr(hostname, m)()
    if result != expected:
        print('{} FAIL: {.hostname} {} != {}'.format(
            m, hostname, result, expected))
    else:
        print('{} PASS: {.hostname} {}'.format(m, hostname, result))


def test_tls():
    testdata = (
        ('abba[mnop]qrst', True),
        ('abcd[bddb]xyyx', False),
        ('aaaa[qwer]tyui', False),
        ('ioxxoj[asdfgh]zxcvbn', True),
    )
    for hostname, expected in testdata:
        test(Hostname(hostname), expected, 'supports_tls')


def test_ssl():
    testdata = (
        ('aba[bab]xyz', True),
        ('xyx[xyx]xyx', False),
        ('aaa[kek]eke', True),
        ('zazbz[bzb]cdb', True),
    )
    for hostname, expected in testdata:
        test(Hostname(hostname), expected, 'supports_ssl')


if __name__ == '__main__':
    if '-t' in sys.argv[1:]:
        test_tls()
        test_ssl()
        sys.exit(0)

    tls_count = 0
    ssl_count = 0
    with open(os.path.join(HERE, 'puzzle07_input.txt')) as hostnames:
        for line in hostnames:
            hostname = Hostname(line.strip())
            tls_count += hostname.supports_tls()
            ssl_count += hostname.supports_ssl()

    print('Star 1:', tls_count)
    print('Star 2:', ssl_count)
