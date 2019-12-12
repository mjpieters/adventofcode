import os.path
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def decode_by_freq(lines):
    counts = []
    for line in lines:
        line = line.strip()
        if not counts:
            counts = [Counter() for _ in range(len(line))]
        for c, counter in zip(line, counts):
            counter[c] += 1
    most_common = ''.join([max(count, key=count.get) for count in counts])
    least_common = ''.join([min(count, key=count.get) for count in counts])
    return most_common, least_common


testdata = '''\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
'''.splitlines()

testmost, testleast = decode_by_freq(testdata)
print('Test:', testmost, testleast)

with open(os.path.join(HERE, 'puzzle06_input.txt')) as messages:
    most, least = decode_by_freq(messages)
    print('Star 1:', most)
    print('Star 2:', least)
