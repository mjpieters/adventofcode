import os
import subprocess
import sys


def plugin(year, day, data):
    source = f"{year}/Day {day:02d}.ipynb"
    part1 = part2 = None
    if os.path.isfile(source):
        args = ["jupyter", "nbconvert", "--to=python", source]
        subprocess.check_output(args, stderr=subprocess.STDOUT)
        script = source.replace(".ipynb", ".py")
        output = subprocess.check_output([sys.executable, script], encoding="utf-8")
        for line in output.splitlines():
            if line.startswith("Part 1:"):
                part1 = line[7:].strip()
            if line.startswith("Part 2:"):
                part2 = line[7:].strip()
    return part1, part2
