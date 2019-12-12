import os
from ast import literal_eval

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'inputs/input8.txt')

# quick and dirty way; have Python do the parsing
diff1 = diff2 = 0
for l in open(filename):
    diff1 += len(l) - len(literal_eval(l))
    diff2 += 2 + l.count('"') + l.count('\\')

print('Part 1:', diff1)
print('Part 2:', diff2)
