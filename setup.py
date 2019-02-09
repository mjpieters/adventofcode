from setuptools import setup

setup(
    name="advent-of-code-martijn",
    version="0.1",
    url="https://github.com/mjpieters/adventofcode",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=["advent-of-code-data >= 0.8.0"],
    python_requires=">= 3.7",
    py_modules=["entrypoint"],
    entry_points={"adventofcode.user": ["martijn = entrypoint:plugin"]},
)
