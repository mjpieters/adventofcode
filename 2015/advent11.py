from string import ascii_lowercase
from itertools import chain, permutations, product
import bisect
import re
import time


letters = ''.join([l for l in ascii_lowercase if l not in 'ilo'])
# 21 valid 3-letter consecutive sequences
sequences = [''.join(seq)
             for seq in zip(
                 ascii_lowercase, ascii_lowercase[1:], ascii_lowercase[2:])
             if not any(c in 'ilo' for c in seq)]


def generate_next(password):
    # no z, this is deliberate! The KeyError signals we need to recurse
    next_map = {a: b for a, b in zip(letters, letters[1:])}
    # Technically speaking, we would need to account for i, l and o too,
    # since Santa may have used those in the old password
    next_map.update({'i': 'j', 'l': 'm', 'o': 'p'})

    def increment(pw):
        try:
            return pw[:-1] + next_map[pw[-1]]
        except KeyError:
            return increment(pw[:-1]) + 'a'

    has_seq = re.compile(r'({})'.format('|'.join(sequences)))
    has_doubles = re.compile(r'(.)\1.*(.)\2')

    while True:
        password = increment(password)
        if bool(has_seq.search(password) and has_doubles.search(password)):
            return password


def generate_all():
    # There are only 15 ^ 5  possible 3-character consequtive sequences in the
    # passwords. Combined with the requirement there are 2 doubled letter
    # pairs, limits the total to 6712592 (6.7 million) different passwords
    doubled = [l + l for l in letters]

    print('Generating all possible passwords')
    start = time.time()
    all_passwords = sorted(set(chain(
        # no overlap between sequence and doubled letters
        (''.join(c)
         for p in product(sequences, letters, doubled, doubled)
         for c in permutations(p)),
        # last letter of sequence doubled
        (''.join(c)
         for p in product((s + s[-1] for s in sequences),
                          doubled, *[letters] * 2)
         for c in permutations(p)),
        # first letter of sequence doubled
        (''.join(c)
         for p in product((s[0] + s for s in sequences),
                          doubled, *[letters] * 2)
         for c in permutations(p)),
        # first and last letter of sequence doubled
        (''.join(c)
         for p in product((s[0] + s + s[-1] for s in sequences),
                          *[letters] * 3)
         for c in permutations(p)),
    )))
    print('Done generating all {} possible passwords in {:.3f} seconds'.format(
        len(all_passwords), time.time() - start))
    return all_passwords


if __name__ == '__main__':
    import sys
    old_password = sys.argv[-1]

    if '--gen' in sys.argv:
        all_passwords = generate_all()
        new_password = all_passwords[
            bisect.bisect_right(all_passwords, old_password)]
        print('Part 1:', new_password)
        next_password = all_passwords[
            bisect.bisect_right(all_passwords, new_password)]
        print('Part 2:', next_password)
    else:
        new_password = generate_next(old_password)
        print('Part 1:', new_password)
        next_password = generate_next(new_password)
        print('Part 2:', next_password)
