# Advent of code solutions

**Author**: [Martijn Pieters](https://www.zopatista.com)  
**Twitter**: [@zopatista](https://twitter.com/zopatista)  
**GitHub**: [mjpieters](https://github.com/mjpieters)  

These are my [Advent of Code][AoC] puzzle solutions.

All solutions use [Python 3.7][pydotorg], and are presented in [Jupyter notebooks][jupyter] for easy [viewing on GitHub][github] or the [online Jupyter notebook viewer][nbviewer].

I don't aim to be first on any leaderboard. I aim to have fun solving the coding puzzles and playing with the concepts, and I try to include explanations of my thinking in the notebooks. Sometimes that means I'll include an animation or graph to show off some aspect of the puzzle.

## Running locally

Everything here is run through Jupyter notebooks. If you check out this repository locally everything is included to recreate my environment.

I use [Pipenv][pipenv] to manage dependencies, make sure you [have it installed][pipenv_install] before continuing. Once installed, run

```
$ pipenv install
$ ./start
```

and the jupyter notebook interface is automatically opened in your default browser. You can stop the server with the *Quit* button in the web interface, or with the `./stop` script.

Everything is organised in per-year folders.

## Puzzle input files

**Note**: I do not include the puzzle inputs, as these are unique to each Advent of Code participant. You can get these trivially by creating your own [Advent of Code][AoC] account, and downloading the puzzle inputs yourself.

Each puzzle loads input from the relative 'inputs' directory, in the form `inputs/day##.txt`.

I may in future start using Wim Glenn's [`advent-of-code-data` package][aocdata] to load data files instead.

## License

See the [LICENSE file](LICENSE) in the same directory.

---

[jupyter]: http://jupyter.org/
[AoC]: https://adventofcode.com/
[pydotorg]: https://python.org
[github]: https://github.com/mjpieters/adventofcode/tree/master/
[nbviewer]: https://nbviewer.jupyter.org/github/mjpieters/adventofcode/tree/master/
[pipenv]: https://pipenv.readthedocs.io/
[pipenv_install]: https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv
[aocdata]: https://pypi.org/project/advent-of-code-data/
