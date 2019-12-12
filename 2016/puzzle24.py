import os.path
from heapq import heapify, heappush, heappop
from itertools import combinations, count, permutations


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


class MazeState:
    def __init__(self, x, y, maze, steps=0):
        self.x, self.y = x, y
        self.maze = maze
        self.steps = steps

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return '<MazeState({0.x}, {0.y}, {0.steps})>'.format(self)

    def moves(self):
        m = self.maze
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x, y = self.x + dx, self.y + dy
            if 0 <= x < len(m) and 0 <= y < len(m[0]) and m[x][y] != '#':
                yield MazeState(x, y, m, self.steps + 1)

    def heuristic(self, target):
        return abs(self.x - target.x) + abs(self.y - target.y) + self.steps


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

        if current == goal:
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


def quickest_path(maze, return_=False):
    points = {p: MazeState(x, y, maze)
              for x, row in enumerate(maze)
              for y, p in enumerate(row) if p.isdigit()}
    distances = {frozenset([start, goal]): shortest_path(
                     points[start], points[goal])
                 for start, goal in combinations(points, 2)}

    def distance(path):
        return sum(distances[frozenset([a, b])] for a, b in zip(path, path[1:]))

    return min(distance(('0',) + p + (('0',) if return_ else ()))
               for p in permutations(points.keys() - {'0'}))


def test():
    print('Star 1 test')
    maze = '''\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
'''.splitlines()
    assert quickest_path(maze) == 14

    # print('Star 2 test')
    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    with open(os.path.join(HERE, 'puzzle24_input.txt'), 'r') as mazedata:
        maze = [line.strip() for line in mazedata]

    print('Star 1:', quickest_path(maze))
    print('Star 2:', quickest_path(maze, return_=True))
