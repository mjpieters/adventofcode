from collections import deque
from hashlib import md5
from heapq import heapify, heappush, heappop
from itertools import count


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


DIR = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}


class MazeState:
    def __init__(self, key, x=0, y=0, path=''):
        self.key = key
        self.x, self.y = x, y
        self.path = path
        doorhash = md5(bytes(key + path, 'ascii')).hexdigest()
        self.opendoors = {d: h in 'bcdef' for d, h in zip('UDLR', doorhash)}

    def __eq__(self, other):
        return (self.x, self.y, self.path) == (other.x, other.y, other.path)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.path)

    def __repr__(self):
        return (
            '<MazeState({0.key!r}, x={0.x}, y={0.y}, path={0.path!r})>'.format(
                self))

    def moves(self):
        for d, (dx, dy) in DIR.items():
            x, y = self.x + dx, self.y + dy
            if self.opendoors[d] and 0 <= x < 4 and 0 <= y < 4:
                yield MazeState(self.key, x, y, self.path + d)

    def heuristic(self):
        return len(self.path) + (3 - self.x) + (3 - self.y)


def shortest_path(start):
    queue = PriorityQueue((start.heuristic(), start))
    closed = set()

    while queue:
        current = queue.get()

        if (current.x, current.y) == (3, 3):
            return current.path

        closed.add(current)
        for neighbor in current.moves():
            if neighbor in closed:
                continue
            queue.put(neighbor.heuristic(), neighbor)


def longest_path(start):
    queue = deque([start])
    maxlength = 0

    while queue:
        current = queue.popleft()
        for neighbor in current.moves():
            if (neighbor.x, neighbor.y) == (3, 3):
                maxlength = max(maxlength, len(neighbor.path))
                continue
            queue.append(neighbor)

    return maxlength


def test():
    print('Star 1 test')
    assert shortest_path(MazeState('hijkl')) is None
    assert shortest_path(MazeState('ihgpwlah')) == 'DDRRRD'
    assert shortest_path(MazeState('kglvqrro')) == 'DDUDRLRRUDRD'
    assert shortest_path(MazeState('ulqzkmiv')) == (
        'DRURDRUDDLLDLUURRDULRLDUUDDDRR')

    print('Star 2 test')
    assert longest_path(MazeState('ihgpwlah')) == 370
    assert longest_path(MazeState('kglvqrro')) == 492
    assert longest_path(MazeState('ulqzkmiv')) == 830

    print('Tests passed')


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    key = 'qljzarfv'
    start = MazeState(key)
    print('Star 1:', shortest_path(start))
    print('Star 2:', longest_path(start))
