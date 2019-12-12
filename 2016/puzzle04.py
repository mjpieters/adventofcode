import os.path
from collections import Counter
from heapq import nsmallest
from string import ascii_lowercase

HERE = os.path.dirname(os.path.abspath(__file__))


def name_parts(roomname):
    name, _, checksum = roomname.partition('[')
    checksum = list(checksum.rstrip(']\n'))
    name, _, sector = name.rpartition('-')
    return name, int(sector), checksum


def is_real(roomname):
    name, sector, checksum = name_parts(roomname)
    letter_counts = Counter(name.replace('-', ''))
    most_common = nsmallest(
        5, letter_counts, key=lambda i: (-letter_counts[i], i))
    return most_common == checksum


def decrypt(roomname):
    name, sector, _ = name_parts(roomname)
    shift = sector % 26
    key = (ascii_lowercase * 2)[shift:shift + 26]
    return name.translate(str.maketrans(ascii_lowercase + '-', key + ' '))


with open(os.path.join(HERE, 'puzzle04_input.txt')) as rooms:
    total = sum(name_parts(room)[1] for room in rooms if is_real(room))
    print('Star 1:', total)

with open(os.path.join(HERE, 'puzzle04_input.txt')) as rooms:
    for room in rooms:
        if is_real(room):
            name = decrypt(room)
            if name == 'northpole object storage':
                print('Star 2:', name_parts(room)[1])
                break
