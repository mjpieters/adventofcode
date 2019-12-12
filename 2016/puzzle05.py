from itertools import count
from hashlib import md5


def doorcharacters(doorid):
    doorid_templ = '{}%d'.format(doorid).encode('ascii')
    counter = count()
    while True:
        hashhex = md5(doorid_templ % next(counter)).hexdigest()
        if hashhex[:5] == '00000':
            yield hashhex[5], hashhex[6]


doorid = 'ojvtpuvg'
charpos = doorcharacters(doorid)

star1result = []
star2result = [None] * 8
star2found = 0
while star2found < 8:
    pos, char = next(charpos)
    if len(star1result) < 8:
        star1result.append(pos)
    pos = int(pos, 16)
    if pos < 8 and star2result[pos] is None:
        star2result[pos] = char
        star2found += 1

print('Star 1:', ''.join(star1result))
print('Star 2:', ''.join(star2result))
