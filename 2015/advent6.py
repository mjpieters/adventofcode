import re

from itertools import product
from collections import defaultdict

try:
    from PIL import Image
except ImportError:
    Image = None


class Grid(object):
    _line_pat = re.compile(
        r'(?:(?:turn (on|off))|(toggle)) (\d+),(\d+) through (\d+),(\d+)')

    def __init__(self):
        self._lights = set()

    def __len__(self):
        return len(self._lights)

    def _gen_grid(self, x1, y1, x2, y2):
        return product(range(x1, x2 + 1), range(y1, y2 + 1))

    def process_line(self, line):
        match = self._line_pat.search(line)
        if not match:
            return
        state, toggle = match.group(1, 2)
        x1, y1, x2, y2 = map(int, match.group(3, 4, 5, 6))

        if state == 'on':
            self._lights.update(self._gen_grid(x1, y1, x2, y2))
        elif state == 'off':
            self._lights.difference_update(self._gen_grid(x1, y1, x2, y2))
        else:
            grid = set(self._gen_grid(x1, y1, x2, y2))
            switch_on = grid - self._lights
            self._lights -= grid & self._lights
            self._lights |= switch_on


# tests
g = Grid()
g.process_line('turn on 0,0 through 999,999')
assert len(g) == 1000000

g = Grid()
g.process_line('toggle 0,0 through 999,0')
assert len(g) == 1000

g = Grid()
g.process_line('turn on 0,0 through 499,0')
g.process_line('toggle 0,0 through 999,0')
assert len(g) == 500

g = Grid()
g.process_line('turn on 499,0 through 500,999')
g.process_line('turn off 499,499 through 500,500')
assert len(g) == (2000 - 4)


class BrightnessGrid(Grid):
    def __init__(self):
        self._lights = [[0 for _ in range(1000)] for _ in range(1000)]
        self._brightness = 0

    def __len__(self):
        return self._brightness

    def process_line(self, line):
        match = self._line_pat.search(line)
        if not match:
            return
        state, toggle = match.group(1, 2)
        x1, y1, x2, y2 = map(int, match.group(3, 4, 5, 6))

        lights = self._lights
        coords = self._gen_grid(x1, y1, x2, y2)
        if state == 'on' or toggle:
            amount = 2 if toggle else 1
            for x, y in coords:
                lights[x][y] += amount
                self._brightness += amount
        else:
            for x, y in coords:
                if lights[x][y] > 0:
                    lights[x][y] -= 1
                    self._brightness -= 1


g = BrightnessGrid()
g.process_line('turn on 0,0 through 0,0')
assert len(g) == 1

g.process_line('toggle 0,0 through 999,999')
assert len(g) == 2000001

g.process_line('turn off 0,0 through 999,999')
assert len(g) == 1000001

g.process_line('turn off 0,0 through 999,999')
assert len(g) == 1

g.process_line('turn off 0,0 through 999,999')
assert len(g) == 0


if Image is not None:
    class ImageGrid(Grid):
        def __init__(self):
            self._lights = Image.new('L', (1000, 1000), 0)

        def process_line(self, line):
            match = self._line_pat.search(line)
            if not match:
                return
            state, toggle = match.group(1, 2)
            box = [int(c) for c in match.group(3, 4, 5, 6)]

            lights = self._lights
            region = lights.crop(box)
            if state == 'on':
                region = region.point(lambda p: 255)
            elif state == 'off':
                region = region.point(lambda p: 0)
            else:
                region = region.point(lambda p: 255 - p)
            lights.paste(region, box)

        def save(self, filename):
            self._lights.save(filename)


    class BrightnessImageGrid(ImageGrid, BrightnessGrid):
        def process_line(self, line):
            match = self._line_pat.search(line)
            if not match:
                return
            state, toggle = match.group(1, 2)
            box = [int(c) for c in match.group(3, 4, 5, 6)]

            lights = self._lights
            region = lights.crop(box)
            if state == 'on' or toggle:
                amount = 10 if toggle else 5
                region = region.point(lambda p: p + amount)
            else:
                region = region.point(lambda p: max(0, p - 5))
            lights.paste(region, box)


if __name__ == '__main__':
    import sys
    import os.path

    filename = sys.argv[-1]

    if '-1' in sys.argv:
        g = Grid()
        with open(filename) as f:
            for line in f:
                g.process_line(line)
        print('First part:', len(g))

    if '-2' in sys.argv:
        bg = BrightnessGrid()
        with open(filename) as f:
            for line in f:
                bg.process_line(line)
        print('Second part:', len(bg))

    if Image is not None:
        if '-img1' in sys.argv:
            output = os.path.join(
                os.path.dirname(filename),
                os.path.splitext(os.path.basename(filename))[0] + '_img1.png')
            ig = ImageGrid()
            with open(filename) as f:
                for line in f:
                    ig.process_line(line)
            ig.save(output)
            print('Saved', output)

        if '-img2' in sys.argv:
            output = os.path.join(
                os.path.dirname(filename),
                os.path.splitext(os.path.basename(filename))[0] + '_img2.png')
            big = BrightnessImageGrid()
            with open(filename) as f:
                for line in f:
                    big.process_line(line)
            big.save(output)
            print('Saved', output)
