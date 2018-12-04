# Advent of code solutions

**Author**: [Martijn Pieters](https://www.zopatista.com)  
**Twitter**: [@zopatista](https://twitter.com/zopatista)  
**GitHub**: [mjpieters](https://github.com/mjpieters)  

These are my [Advent of Code][AoC] (AoC) puzzle solutions.

All solutions use [Python 3.7][pydotorg], and are presented in [Jupyter notebooks][jupyter] for easy [viewing on GitHub][github] or the [online Jupyter notebook viewer][nbviewer].

I don't aim to be first on any leaderboard. I aim to have fun solving the coding puzzles and playing with the concepts, and I try to include explanations of my thinking in the notebooks. Sometimes that means I'll include an animation or graph to show off some aspect of the puzzle.

## Running locally

Everything here is run through Jupyter notebooks. If you check out this repository locally everything is included to recreate my environment.

I use [Pipenv][pipenv] to manage dependencies, make sure you [have it installed][pipenv_install] before continuing. Once installed, run

```sh
$ pipenv install
$ ./start
```

and the jupyter notebook interface is automatically opened in your default browser. You can stop the server with the *Quit* button in the web interface, or with the `./stop` script.

Everything is organised in per-year folders.

## Puzzle input data

I have started to use Wim Glenn's [`advent-of-code-data` package][aocdata] to load data directly from the AoC website. This library requires your AoC session cookie. You'll have create your own [Advent of Code][AoC] account, then use your browser development tools to retrieve the session cookie value, then store it according to the `advent-of-code-data` instructions. Since this project uses Pipenv, I store it in a `.env` file in the root directory of this project:

```sh
AOC_SESSION=deadbeafdeadbeafdeadbeafdeadbeafdeadbeafdeadbeafdeadbeafdeadbeaf
```

Do make sure to restart the jupyter notebook server after updating this file.

For older puzzles that I haven't yet updated, I do not include the puzzle inputs, as these are unique to each Advent of Code participant. You can get these trivially by downloading the puzzle inputs yourself using your own AoC account.

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
