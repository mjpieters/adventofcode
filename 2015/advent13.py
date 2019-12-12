from itertools import islice, permutations
import re


def circular_window(seq, n=2):
    it = iter(seq + seq[:n - 1])
    result = tuple(islice(it, n))
    yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def calculate_happiness_change(graph, order):
    return sum(graph[m][l] + graph[m][r]
               for l, m, r in circular_window(order, 3))


def find_max_happiness_change(graph):
    return max(calculate_happiness_change(graph, o)
               for o in permutations(graph))


def read_input(fileobj):
    linepattern = re.compile(
        r'(\w+) would (gain|lose) (\d+) happiness units '
        r'by sitting next to (\w+).')
    graph = {}
    for line in fileobj:
        match = linepattern.search(line)
        if not match:
            continue
        name1, direction, change, name2 = match.groups()
        change = int(change) if direction == 'gain' else -int(change)
        graph.setdefault(name1, {})[name2] = change
    return graph


if __name__ == '__main__':
    import os.path
    import sys
    filename = sys.argv[-1]
    with open(filename) as inf:
        graph = read_input(inf)
    print('Part 1:', find_max_happiness_change(graph))

    for name in graph:
        graph[name]['Myself'] = 0
    graph['Myself'] = dict.fromkeys(graph, 0)
    print('Part 2:', find_max_happiness_change(graph))

    if '--graph' in sys.argv:
        dirname, basename = os.path.split(filename)
        output = os.path.join(dirname, os.path.splitext(basename)[0] + '.dot')
        order = max((o for o in permutations(graph)),
                    key=lambda o: calculate_happiness_change(graph, o))
        with open(output, 'w') as df:
            df.write('graph advent_seating {\nlayout="circo";\n')
            for name, toright in circular_window(order, 2):
                df.write(
                    'n{0} [shape=circle, label="{0}", width=1]\n'
                    'n{0} -- n{1} '
                    '[headlabel="{2}", taillabel="{3}", '
                    'labeldistance=2];\n'.format(
                        name, toright,
                        graph[name][toright], graph[toright][name]))
            df.write('}\n')
        print('Written graph to', output)
