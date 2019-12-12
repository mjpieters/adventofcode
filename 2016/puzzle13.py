from collections import deque
from heapq import heapify, heappush, heappop
from itertools import count

DESIGNER_FAVOURITE = 1358


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


def is_open(x, y):
    if x < 0 or y < 0:
        return False
    num = x * x + 3 * x + 2 * x * y + y + y * y
    num += DESIGNER_FAVOURITE
    return format(num, 'b').count('1') % 2 == 0


class MazeState:
    def __init__(self, x, y, steps=0):
        self.x, self.y = x, y
        self.steps = steps

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return '<MazeState({0.x}, {0.y}, {0.steps})>'.format(self)

    def moves(self):
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            x, y = self.x + dx, self.y + dy
            if is_open(x, y):
                yield MazeState(x, y, self.steps + 1)

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


def reachable(start, steps):
    visited = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for neighbor in current.moves():
            if neighbor.steps <= 50 and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return len(visited)


def test():
    global DESIGNER_FAVOURITE
    DESIGNER_FAVOURITE = 10
    length = shortest_path(MazeState(1, 1), MazeState(7, 4))
    assert length == 11


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        test()
        sys.exit(0)

    length = shortest_path(MazeState(1, 1), MazeState(31, 39))
    print('Star 1:', length)
    reachable_count = reachable(MazeState(1, 1), 50)
    print('Star 2:', reachable_count)
