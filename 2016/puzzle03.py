import os.path
from itertools import islice

HERE = os.path.dirname(os.path.abspath(__file__))


def possible(*sides, pos=set(range(3))):
    return all(sum(sides[i] for i in (pos - {third})) > sides[third]
               for third in pos)

count = 0
with open(os.path.join(HERE, 'puzzle03_input.txt')) as triangles:
    for line in triangles:
        if not line.strip():
            continue
        sides = map(int, line.split())
        if possible(*sides):
            count += 1

print('Star 1:', count)

count = 0
with open(os.path.join(HERE, 'puzzle03_input.txt')) as triangles:
    while True:
        cols = map(str.split, islice(triangles, 3))
        triangle_sides = [map(int, row) for row in zip(*cols)]
        if not triangle_sides:
            break
        for sides in triangle_sides:
            if possible(*sides):
                count += 1

print('Star 2:', count)
