import io
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType

import nbformat


def blacklisted(cell):
    if cell["cell_type"] != "code":
        return True
    if "plt.figure()" in cell["source"]:
        return True
    if "graphviz" in cell["source"]:
        return True


def transform(line):
    prefix = (
        "%",  # IPython magics
        "plot_area(",
        "visualise(",
    )
    if line.startswith(prefix):
        line = "# " + line
    return line


def plugin(year, day, data):
    if year == 2017 and day in {10, 14} and "knothash" not in sys.modules:
        load_knothash_module()
    fname = f"{year}/Day {day:02d}.ipynb"
    part1 = part2 = None
    if os.path.isfile(fname):
        nb = nbformat.read(fname, nbformat.NO_CONVERT)
        sources = [cell["source"] for cell in nb["cells"] if not blacklisted(cell)]
        lines = [s for source in sources for s in source.splitlines()]
        source = "\n".join([transform(line) for line in lines])
        string_io = io.StringIO()
        with redirect_stdout(string_io):
            exec(source, globals())
        output = string_io.getvalue()
        for line in output.splitlines():
            if line.startswith("Part 1:"):
                part1 = line[7:].strip()
            if line.startswith("Part 2:"):
                part2 = line[7:].strip()
    return part1, part2


def load_knothash_module():
    """Import the knothash.py dependency for 2017 Day 10 and Day 14. More difficult than it
    needs to be, because the directory name "2017" is not a valid package name in Python.
    """
    path = Path(__file__).parent / "2017" / "knothash.py"
    mod = sys.modules["knothash"] = ModuleType("knothash")
    exec(path.read_text(), mod.__dict__)
