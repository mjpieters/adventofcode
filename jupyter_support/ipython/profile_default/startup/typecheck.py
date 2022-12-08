"""
Add mypy type-checking cell magic to jupyter/ipython.

Save this script to your ipython profile's startup directory.

IPython's directories can be found via `ipython locate [profile]` to find the current ipython directory and ipython profile directory, respectively.

For example, this file could exist on a path like this on mac:

/Users/yourusername/.ipython/profile_default/startup/typecheck.py

where /Users/yourusername/.ipython/profile_default/ is the ipython directory for
the default profile.

The line magic is called "typecheck" to avoid namespace conflict with the mypy
package.

"""

from IPython.core.magic import register_cell_magic


@register_cell_magic
def typecheck(line, cell):
    """
    Run the following cell though mypy.

    Any parameters that would normally be passed to the mypy cli
    can be passed on the first line, with the exception of the
    -c flag we use to pass the code from the cell we want to execute

     i.e.

    %%typecheck --ignore-missing-imports
    ...
    ...
    ...

    mypy stdout and stderr will print prior to output of cell. If there are no conflicts,
    nothing will be printed by mypy.
    """

    from IPython import get_ipython
    from mypy import api

    mypy_result = api.run(line.split() + ['-c', cell])

    if mypy_result[0]:  # print mypy stdout
        print(mypy_result[0])

    if mypy_result[1]:  # print mypy stderr
        print(mypy_result[1])

    shell = get_ipython()
    shell.run_cell(cell)