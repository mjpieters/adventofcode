import io
import sys
from contextlib import contextmanager
from contextlib import redirect_stdout
from pathlib import Path

import nbformat


here = Path(__file__).parent


def blacklisted(cell):
    if cell["cell_type"] != "code":
        return True
    if "plt.figure()" in cell["source"]:
        return True
    if "graphviz" in cell["source"]:
        return True
    if "plot_license" in cell["source"]:
        return True
    if "from IPython.display import Markdown" in cell["source"]:
        return True


def transform(line):
    prefix = (
        "%",  # IPython magics
        "plot_area",
        "visualise",
        "plot_graph",
        "plot_execution",
        "animate",
    )
    if line.startswith(prefix):
        line = "# " + line
    return line


@contextmanager
def sys_path_augment(path):
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.remove(path)


def plugin(year, day, data):
    dirname = str(year)
    fname = f"Day {day:02d}.ipynb"
    path = here / dirname / fname
    part1 = part2 = None
    if path.is_file():
        nb = nbformat.read(str(path), nbformat.NO_CONVERT)
        sources = [cell["source"] for cell in nb["cells"] if not blacklisted(cell)]
        lines = [s for source in sources for s in source.splitlines()]
        source = "\n".join([transform(line) for line in lines])
        string_io = io.StringIO()
        with redirect_stdout(string_io), sys_path_augment(str(path.parent)):
            exec(source, globals())
        output = string_io.getvalue()
        for line in output.splitlines():
            if line.startswith("Part 1:"):
                part1 = line[7:].strip()
            if line.startswith("Part 2:"):
                part2 = line[7:].strip()
    return part1, part2
