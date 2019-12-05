# Advent of code solutions

**Author**: [Martijn Pieters](https://www.zopatista.com)  
**Twitter**: [@zopatista](https://twitter.com/zopatista)  
**GitHub**: [mjpieters](https://github.com/mjpieters)  

These are my [Advent of Code][AoC] (AoC) puzzle solutions.

All solutions use [Python 3.8][pydotorg], and are presented in [Jupyter notebooks][jupyter] for easy [viewing on GitHub][github] or the [online Jupyter notebook viewer][nbviewer].

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

## Additional dependencies

* Animations are produced using [matplotlib's animation API][mplanimation], which requires [ffmpeg][ffmpeg] to be installed. On Mac OS X just use `brew install ffmpeg`.

* Graphs are plotted using [graphviz](http://www.graphviz.org/) command-line tools such as `dot`, `neato`, and `tred`. On Mac OS X, just use `brew install graphviz`.

## Puzzle input data

I use Wim Glenn's [`advent-of-code-data` package][aocdata] to load data directly from the AoC website. This library requires your AoC session cookie. You'll have create your own [Advent of Code][AoC] account, then use your browser development tools to retrieve the session cookie value. Store the value according to the `advent-of-code-data` instructions (either in `~/.config/aocd/token` or in the `AOC_SESSION` environment variable).

Since this project uses Pipenv, I store it in a `.env` file in the root directory of this project:

```sh
AOC_SESSION=deadbeafdeadbeafdeadbeafdeadbeafdeadbeafdeadbeafdeadbeafdeadbeaf
```

Do make sure to restart the jupyter notebook server after updating this file.

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
[mplanimation]: https://matplotlib.org/api/animation_api.html
[ffmpeg]: https://www.ffmpeg.org/
[aocdata]: https://pypi.org/project/advent-of-code-data/
