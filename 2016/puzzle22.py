import os.path

from bisect import bisect_left
from collections import namedtuple
from heapq import heapify, heappush, heappop
from itertools import count, islice
from operator import attrgetter


HERE = os.path.dirname(os.path.abspath(__file__))


class PriorityQueue:
    def __init__(self, *initial):
        self._queue = []
        self._count = count()
        for pri, item in initial:
            self.put(pri, item)
        heapify(self._queue)

    def __len__(self):
        return len(self._queue)

    def put(self, pri, item):
        heappush(self._queue, (pri, next(self._count), item))

    def get(self):
        if not self:
            raise ValueError('Queue is empty')
        return heappop(self._queue)[-1]


class Server(namedtuple('ServerBase', 'x y size used available perc')):
    @classmethod
    def from_line(cls, line):
        fs, *sizes, perc = line.split()
        size, used, avail = (int(v.rstrip('T')) for v in sizes)
        x, y = (int(v.lstrip('xy')) for v in fs.split('-')[-2:])
        return cls(x, y, size, used, avail, int(perc.rstrip('%')))


GridInfo = namedtuple('GridInfo', 'constraints avail grid')


class State:
    def __init__(self, focus, gridinfo, steps=0):
        self.focus = focus
        self.gridinfo = gridinfo
        self.steps = steps

    def __eq__(self, other):
        return self.focus == other.focus

    def __hash__(self):
        return hash(self.focus)

    def __repr__(self):
        return '<State(({0.focus[0]}, {0.focus[1]}), {0.steps})>'.format(
            self)

    def moves(self):
        cols, rows = self.gridinfo.constraints
        avail, grid = self.gridinfo.avail, self.gridinfo.grid
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x, y = self.focus[0] + dx, self.focus[1] + dy
            if not (0 <= x < cols and 0 <= y < rows):
                continue
            if grid[x][y].used > avail:
                # this server can never offload their data *anywhere*
                continue
            yield State((x, y), self.gridinfo, self.steps + 1)

    def heuristic(self, target):
        x, y = self.focus
        return abs(x - target.x) + abs(y - target.y) + self.steps


def shortest_path(start, goal):
    queue = PriorityQueue((start.heuristic(goal), start))
    open_ = {start: 0}
    closed = set()

    while open_:
        current = queue.get()
        if open_.get(current) != current.steps:
            # ignore items in the queue for which a shorter
            # path exists
            continue

        if current.focus == (goal.x, goal.y):
            return current.steps

        del open_[current]
        closed.add(current)
        for neighbor in current.moves():
            if neighbor in closed:
                continue
            if neighbor.steps >= open_.get(neighbor, float('inf')):
                    # not a shorter path than we already have
                    continue
            open_[neighbor] = neighbor.steps
            queue.put(neighbor.heuristic(goal), neighbor)


def free_data(servers):
    cols = max(s.x for s in servers) + 1
    rows = max(s.y for s in servers) + 1
    avail = max(s.available for s in servers)
    empty_server = next(s for s in servers if s.used == 0)
    grid = [[None] * rows for _ in range(cols)]
    for s in servers:
        grid[s.x][s.y] = s
    gridinfo = GridInfo((cols, rows), avail, grid)

    # two stages to solve:
    # 1) get the empty data spot to the target server
    start = State((empty_server.x, empty_server.y), gridinfo)
    part1 = shortest_path(start, grid[cols - 1][0])
    # 2) get the target server data to (0, 0); the target is in actual
    #    fact already 1 step closer, and each step is actually 5 to move
    #    the hole around and move the server data.
    start = State((grid[cols - 1][0].x, grid[cols - 1][0].y), gridinfo)
    part2 = (shortest_path(start, grid[0][0]) - 1) * 5

    return part1 + part2


def count_viable(servers):
    byavail = sorted(servers, key=attrgetter('available'))
    availability = [s.available for s in byavail]
    total = 0
    for i, server in enumerate(byavail):
        if not server.used:
            continue
        insertion_pos = bisect_left(availability, server.used)
        viable = len(availability) - insertion_pos
        if insertion_pos < i:
            # remove this server from the count
            viable -= 1
        total += viable
    return total


def test():
    print('Star 2 test')
    servers = [Server.from_line(l) for l in '''\
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
'''.splitlines()]
    assert free_data(servers) == 7

    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    with open(os.path.join(HERE, 'puzzle22_input.txt'), 'r') as nodes:
        servers = [Server.from_line(l) for l in islice(nodes, 2, None)]

    print('Star 1:', count_viable(servers))
    print('Star 2:', free_data(servers))
